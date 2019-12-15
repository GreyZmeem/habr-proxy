# -*- coding: utf-8 -*-

import dataclasses

from aiohttp import web
from app.proxy.config import Config, Patcher
from app.proxy.patcher_ivelum import IVelumPatcher, IVelumPatcherConfig
from app.proxy.proxy import Proxy
from app.proxy.req_resp import Request, Response


@dataclasses.dataclass(frozen=True)
class AppConfig(object):
    """AioHTTP application configuration."""

    #: Proxied resource (e.g. `https://habr.com`).
    upstream: str
    #: Length of words to patch.
    length: int
    #: String which must be appended to the matched words.
    append: str


def create_app(config: AppConfig) -> web.Application:
    """Create AioHTTP application."""
    proxy_patcher_config = IVelumPatcherConfig(config.length, config.append)
    proxy_patcher = IVelumPatcher(proxy_patcher_config)
    proxy_config = Config("", config.upstream, proxy_patcher)
    proxy_handler = ProxyHandler(proxy_patcher, proxy_config)

    app = web.Application()
    app.add_routes([
        web.get("/{tail:.*}", proxy_handler.dispatch),
    ])
    return app


class ProxyHandler(object):
    """Wildcard handler which sends all requests through proxy."""

    def __init__(self, proxy_patcher: Patcher, proxy_config: Config):
        self.proxy_patcher = proxy_patcher
        self.proxy_config = proxy_config

    async def dispatch(self, request: web.Request) -> web.Response:
        """Handle HTTP request."""
        proxy = self._proxy(request)
        proxy_request = await _aio_to_proxy(request)
        proxy_response = await proxy.dispatch(proxy_request)
        return await _proxy_to_aio(proxy_response)

    def _proxy(self, request: web.Request) -> Proxy:
        """Create proxy instance for the given request."""
        host = f"{request.scheme}://{request.host}"
        config = dataclasses.replace(self.proxy_config, host=host)
        return Proxy(config)


async def _aio_to_proxy(request: web.Request) -> Request:
    """Build proxy request instance from aiohttp request."""
    url = str(request.url)
    body = await request.read()
    headers = tuple(request.headers.items())
    return Request(url, request.method, headers=headers, body=body)


async def _proxy_to_aio(response: Response) -> web.Response:
    """Build aiohttp response instance from proxy response."""
    headers = dict(response.headers)
    return web.Response(
        body=response.body,
        status=response.status,
        headers=headers,
    )

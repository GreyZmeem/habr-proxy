# -*- coding: utf-8 -*-

import aiohttp
from app.proxy.config import Config
from app.proxy.req_resp import Headers, Request, Response


class Proxy(object):
    """Asd."""

    def __init__(self, config: Config):
        self.config: Config = config

    async def dispatch(self, request: Request) -> Response:
        """Asd."""
        request = self.patch_request(request)
        response = await self.make_request(request)
        return self.patch_response(response)

    def patch_request(self, request: Request) -> Request:
        """Patch HTTP request."""
        hosts = self.config.host, self.config.upstream
        return self.config.patcher(request, hosts)

    def patch_response(self, response: Response) -> Response:
        """Patch HTTP response."""
        hosts = self.config.upstream, self.config.host
        return self.config.patcher(response, hosts)

    async def make_request(self, request: Request) -> Response:
        """Perform HTTP request to the upstream."""
        # TODO: Move this code to separate module and defined as a dependency.
        async with aiohttp.ClientSession() as session:
            req_headers = dict(request.headers)
            response = await session.request(
                url=request.url,
                method=request.method,
                headers=req_headers,
                allow_redirects=False,
                raise_for_status=False,
                verify_ssl=False,
            )
            headers: Headers = tuple(response.headers.items())
            body = await response.read()
            return Response(headers, response.status, body)

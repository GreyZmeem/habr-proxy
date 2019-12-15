# -*- coding: utf-8 -*-

import dataclasses
from http import HTTPStatus
from typing import List, Optional, overload
from urllib.parse import ParseResult, urlparse

from app.proxy import const
from app.proxy.config import Patcher, ReqResp, SrcDst
from app.proxy.req_resp import Header, Headers, Request, Response
from multidict import CIMultiDict


# noinspection PyMethodMayBeStatic
class DefaultPatcher(Patcher):  # noqa: WPS214
    """Default patcher implementation."""

    remove_headers = const.remove_headers

    @overload
    def __call__(
        self,
        req_resp: Request,
        hosts: SrcDst,
    ) -> Request:
        """Patch HTTP request."""

    @overload
    def __call__(  # noqa: F811
        self,
        req_resp: Response,
        hosts: SrcDst,
    ) -> Response:
        """Patch HTTP response."""

    def __call__(  # noqa: F811
        self,
        req_resp: ReqResp,
        hosts: SrcDst,
    ) -> ReqResp:
        """Patch HTTP request / response objects."""
        kwargs = {
            "headers": self.patch_headers(req_resp, hosts),
            "body": self.patch_body(req_resp, hosts),
        }
        if isinstance(req_resp, Request):
            kwargs["url"] = self.patch_url(req_resp, hosts)  # type: ignore
        if isinstance(req_resp, Response):
            if req_resp.status == HTTPStatus.PERMANENT_REDIRECT.value:
                kwargs["status"] = HTTPStatus.FOUND.value  # type: ignore
        return dataclasses.replace(req_resp, **kwargs)

    def patch_headers(self, req_resp: ReqResp, hosts: SrcDst) -> Headers:
        """Patch HTTP request / response headers."""
        new_headers: List[Header] = []
        for header_name, header_value in req_resp.headers:
            header_name = header_name.lower()
            if header_name in self.remove_headers:
                continue
            new_header = self.patch_header((header_name, header_value), hosts)
            new_headers.append(new_header)
        return tuple(new_headers)

    def patch_header(self, header: Header, hosts: SrcDst) -> Header:
        """Patch single HTTP header."""
        src: ParseResult = urlparse(hosts[0])
        dst: ParseResult = urlparse(hosts[1])
        header_name, header_value = header
        header_value = header_value.replace(
            src.scheme or "http",
            dst.scheme or "http",
        )
        header_value = header_value.replace(
            src.netloc,
            dst.netloc,
        )
        return header_name, header_value

    def patch_url(self, req: Request, hosts: SrcDst) -> str:
        """Patch HTTP request url."""
        dst: ParseResult = urlparse(hosts[1])
        url: ParseResult = urlparse(req.url)
        url = url._replace(scheme=dst.scheme, netloc=dst.netloc)  # noqa: WPS437
        return url.geturl()

    def patch_body(self, req_resp: ReqResp, hosts: SrcDst) -> Optional[bytes]:
        """Patch HTTP request / response body."""
        if not self.must_patch_body(req_resp):
            return req_resp.body
        body = req_resp.body.decode("utf-8")  # type: ignore
        body = body.replace(hosts[0], hosts[1])
        return body.encode("utf-8")

    def must_patch_body(self, req_resp: ReqResp) -> bool:
        """Check if request or response body must be patched."""
        if not req_resp.body:
            return False

        content_type = CIMultiDict(req_resp.headers).get("content-type")
        if not content_type or not content_type.lower().startswith("text/html"):
            return False

        return True

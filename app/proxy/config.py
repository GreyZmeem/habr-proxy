# -*- coding: utf-8 -*-

import abc
from dataclasses import dataclass
from typing import Tuple, Union, overload

from app.proxy import const
from app.proxy.req_resp import Request, Response

SrcDst = Tuple[str, str]
ReqResp = Union[Request, Response]


class Patcher(abc.ABC):
    """Protocol describes methods for patching HTTP requests and responses."""

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

    @abc.abstractmethod
    def __call__(  # noqa: F811
        self,
        req_resp: ReqResp,
        hosts: SrcDst,
    ) -> ReqResp:
        """Patch either HTTP request or response."""
        raise NotImplementedError


@dataclass(frozen=True)
class Config(object):
    """Configuration for `Proxy` service."""

    #: Local resource (e.g. `http://127.0.0.1:8080`).
    host: str
    #: Proxied resource (e.g. `https://habr.com`).
    upstream: str
    #: Callable for patching HTTP request / response objects.
    patcher: Patcher
    #: Upstream HTTP request timeout.
    timeout: int = const.timeout

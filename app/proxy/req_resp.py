# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Optional, Set, Tuple

Header = Tuple[str, str]
Headers = Tuple[Header, ...]
HeaderNames = Set[str]


@dataclass(frozen=True)
class Request(object):
    """HTTP request."""

    #: Requested URL.
    url: str
    #: HTTP request method.
    method: str
    #: HTTP request headers.
    headers: Headers = field(default_factory=tuple)
    #: HTTP request body.
    body: Optional[bytes] = None


@dataclass(frozen=True)
class Response(object):
    """HTTP response."""

    #: HTTP response headers.
    headers: Headers = field(default_factory=tuple)
    #: HTTP response status code.
    status: int = HTTPStatus.OK.value
    #: HTTP response body.
    body: Optional[bytes] = None

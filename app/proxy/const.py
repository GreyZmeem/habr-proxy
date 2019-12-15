# -*- coding: utf-8 -*-

from typing import Final, Set

# =======
# General
# =======

#: Default upstream.
upstream: Final[str] = "https://habr.com"
#: List of headers to remove from HTTP requests / responses.
remove_headers: Final[Set[str]] = {
    "accept-encoding",
    "content-encoding",
    "keep-alive",
    "p3p",
    "public-key-pins",
    "strict-transport-security",
    "te",
    "transfer-encoding",
    "upgrade-insecure-requests",
}
#: Upstream request timeout.
timeout: Final[int] = 30

# ==============
# iVelum patcher
# ==============

#: Default word length.
word_length: Final[int] = 6
#: Default text to append.
word_append: Final[str] = "™"

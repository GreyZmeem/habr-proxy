# -*- coding: utf-8 -*-

import dataclasses
import itertools
import unicodedata
from typing import Iterable, Optional, Set

from app.proxy.config import ReqResp, SrcDst
from app.proxy.patcher_default import DefaultPatcher
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from nltk import wordpunct_tokenize


@dataclasses.dataclass(frozen=True)
class IVelumPatcherConfig(object):
    """Configuration for the `IVelumPatcher` service."""

    #: Length of words to patch.
    words_length: int
    #: String which must be appended to the matched words.
    append: str


class IVelumPatcher(DefaultPatcher):
    """Patcher implementation for iVelum code challenge."""

    #: Form of unicode normalization.
    unicode_form: str = "NFKC"
    #: Skip patching these tags.
    skip_tags: Set[str] = {"script", "style"}

    def __init__(self, config: IVelumPatcherConfig):
        self.config = config

    def patch_body(self, req_resp: ReqResp, hosts: SrcDst) -> Optional[bytes]:
        """Iterate over all tags changing its text."""
        if not self.must_patch_body(req_resp):
            return req_resp.body

        body = super().patch_body(req_resp, hosts)
        text = body.decode("utf-8")  # type: ignore

        html = BeautifulSoup(text, "lxml")
        for tag in html.find_all(name=True):
            if tag.name not in self.skip_tags:
                self.patch_tag(tag)

        return html.encode("utf-8")

    def patch_tag(self, tag: Tag):
        """Patch single tag's text."""
        for child_tag in tag.children:
            if not isinstance(child_tag, NavigableString):
                continue
            if child_tag.parent != tag:
                continue
            self.patch_navigable_string(child_tag)

    def patch_navigable_string(self, nav_string: NavigableString):
        """Replace navigable string tag with a patched text."""
        text = unicodedata.normalize(self.unicode_form, nav_string)
        split = ((wordpunct_tokenize(word), " ") for word in text.split())
        words: Iterable[str] = itertools.chain(*list(
            itertools.chain(*split),
        ))
        words = (
            (
                f"{word}{self.config.append}"
                if len(word) == self.config.words_length
                else word
            )
            for word in words
        )
        nav_string.replace_with(NavigableString("".join(words)))

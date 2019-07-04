# coding: utf-8
from __future__ import unicode_literals

import sys
import pytest
from spacy.util import get_lang_class


# fmt: off
# Only include languages with no external dependencies
# excluded: ja, ru, th, uk, vi, zh
LANGUAGES = ["af", "ar", "bg", "bn", "ca", "cs", "da", "de", "el", "en", "es",
             "et", "fa", "fi", "fr", "ga", "he", "hi", "hr", "hu", "id", "is",
             "it", "ja", "kn", "lt", "lv", "nb", "nl", "pl", "pt", "ro", "si",
             "sk", "sl", "sq", "sv", "ta", "te", "tl", "tr", "tt", "ur"]
# fmt: on


@pytest.mark.parametrize("lang", LANGUAGES)
def test_lang_initialize(lang, capfd):
    """Test that languages can be initialized."""
    if lang == 'ja' and sys.version_info < (3, 5):
        return  # SudachiPy does not support < 3.5
    nlp = get_lang_class(lang)()
    # Check for stray print statements (see #3342)
    doc = nlp("test")  # noqa: F841
    captured = capfd.readouterr()
    assert not captured.out

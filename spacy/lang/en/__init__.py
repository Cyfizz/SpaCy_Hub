from thinc.api import Config

from .tokenizer_exceptions import TOKENIZER_EXCEPTIONS
from .stop_words import STOP_WORDS
from .lex_attrs import LEX_ATTRS
from .syntax_iterators import SYNTAX_ITERATORS

from .punctuation import TOKENIZER_INFIXES
from ..tokenizer_exceptions import BASE_EXCEPTIONS
from ...language import Language
from ...attrs import LANG
from ...util import update_exc, registry


DEFAULT_CONFIG = """
[nlp]
lang = "en"

[nlp.lemmatizer]
@lemmatizers = "spacy.Lemmatizer.v1"

[nlp.lemmatizer.data_paths]
@assets = "spacy-lookups-data"
lang = ${nlp:lang}
"""


class EnglishDefaults(Language.Defaults):
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    lex_attr_getters.update(LEX_ATTRS)
    lex_attr_getters[LANG] = lambda text: "en"
    tokenizer_exceptions = update_exc(BASE_EXCEPTIONS, TOKENIZER_EXCEPTIONS)
    stop_words = STOP_WORDS
    syntax_iterators = SYNTAX_ITERATORS
    infixes = TOKENIZER_INFIXES
    single_orth_variants = [
        {"tags": ["NFP"], "variants": ["…", "..."]},
        {"tags": [":"], "variants": ["-", "—", "–", "--", "---", "——"]},
    ]
    paired_orth_variants = [
        {"tags": ["``", "''"], "variants": [("'", "'"), ("‘", "’")]},
        {"tags": ["``", "''"], "variants": [('"', '"'), ("“", "”")]},
    ]


class English(Language):
    lang = "en"
    Defaults = EnglishDefaults
    default_config = Config().from_str(DEFAULT_CONFIG)


__all__ = ["English"]

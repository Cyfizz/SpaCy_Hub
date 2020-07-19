from thinc.api import Config

from .stop_words import STOP_WORDS
from .tokenizer_exceptions import TOKENIZER_EXCEPTIONS
from .lex_attrs import LEX_ATTRS
from ..tokenizer_exceptions import BASE_EXCEPTIONS
from ...language import Language
from ...attrs import LANG
from ...util import update_exc


DEFAULT_CONFIG = """
[nlp]
lang = "sr"

[nlp.lemmatizer]
@lemmatizers = "spacy.Lemmatizer.v1"
data_paths = {"@lookups": "spacy-lookups-data.sr"}
"""


class SerbianDefaults(Language.Defaults):
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    lex_attr_getters.update(LEX_ATTRS)
    lex_attr_getters[LANG] = lambda text: "sr"
    tokenizer_exceptions = update_exc(BASE_EXCEPTIONS, TOKENIZER_EXCEPTIONS)
    stop_words = STOP_WORDS


class Serbian(Language):
    lang = "sr"
    Defaults = SerbianDefaults
    default_config = Config().from_str(DEFAULT_CONFIG)


__all__ = ["Serbian"]

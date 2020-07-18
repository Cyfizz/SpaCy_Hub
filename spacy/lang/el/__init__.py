from thinc.api import Config

from .tokenizer_exceptions import TOKENIZER_EXCEPTIONS
from ..tag_map import TAG_MAP
from .stop_words import STOP_WORDS
from .lex_attrs import LEX_ATTRS
from .lemmatizer import GreekLemmatizer
from .syntax_iterators import SYNTAX_ITERATORS
from .punctuation import TOKENIZER_PREFIXES, TOKENIZER_SUFFIXES, TOKENIZER_INFIXES
from ..tokenizer_exceptions import BASE_EXCEPTIONS
from ...language import Language
from ...lemmatizer import create_lookups
from ...attrs import LANG
from ...util import update_exc, registry


DEFAULT_CONFIG = """
[nlp]
lang = "el"

[nlp.lemmatizer]
@lemmatizers = "spacy.GreekLemmatizer.v1"
"""


@registry.lemmatizers("spacy.GreekLemmatizer.v1")
def create_greek_lemmatizer():
    def lemmatizer_factory(nlp):
        lookups = create_lookups(nlp.lang)
        return GreekLemmatizer(lookups=lookups)

    return lemmatizer_factory


class GreekDefaults(Language.Defaults):
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    lex_attr_getters.update(LEX_ATTRS)
    lex_attr_getters[LANG] = lambda text: "el"
    tokenizer_exceptions = update_exc(BASE_EXCEPTIONS, TOKENIZER_EXCEPTIONS)
    stop_words = STOP_WORDS
    tag_map = TAG_MAP
    prefixes = TOKENIZER_PREFIXES
    suffixes = TOKENIZER_SUFFIXES
    infixes = TOKENIZER_INFIXES
    syntax_iterators = SYNTAX_ITERATORS


class Greek(Language):
    lang = "el"
    Defaults = GreekDefaults
    default_config = Config().from_str(DEFAULT_CONFIG)


__all__ = ["Greek"]

import re
import string

import hypothesis
import hypothesis.strategies
import pytest

import spacy
from spacy.tokenizer import Tokenizer
from spacy.util import get_lang_class

# Only include languages with no external dependencies
# "is" seems to confuse importlib, so we're also excluding it for now
# excluded: ja, ru, th, uk, vi, zh, is
LANGUAGES = [
    pytest.param("fr", marks=pytest.mark.slow()),
    pytest.param("af", marks=pytest.mark.slow()),
    pytest.param("ar", marks=pytest.mark.slow()),
    pytest.param("bg", marks=pytest.mark.slow()),
    "bn",
    pytest.param("ca", marks=pytest.mark.slow()),
    pytest.param("cs", marks=pytest.mark.slow()),
    pytest.param("da", marks=pytest.mark.slow()),
    pytest.param("de", marks=pytest.mark.slow()),
    "el",
    "en",
    pytest.param("es", marks=pytest.mark.slow()),
    pytest.param("et", marks=pytest.mark.slow()),
    pytest.param("fa", marks=pytest.mark.slow()),
    pytest.param("fi", marks=pytest.mark.slow()),
    "fr",
    pytest.param("ga", marks=pytest.mark.slow()),
    pytest.param("he", marks=pytest.mark.slow()),
    pytest.param("hi", marks=pytest.mark.slow()),
    pytest.param("hr", marks=pytest.mark.slow()),
    "hu",
    pytest.param("id", marks=pytest.mark.slow()),
    pytest.param("it", marks=pytest.mark.slow()),
    pytest.param("kn", marks=pytest.mark.slow()),
    pytest.param("lb", marks=pytest.mark.slow()),
    pytest.param("lt", marks=pytest.mark.slow()),
    pytest.param("lv", marks=pytest.mark.slow()),
    pytest.param("nb", marks=pytest.mark.slow()),
    pytest.param("nl", marks=pytest.mark.slow()),
    "pl",
    pytest.param("pt", marks=pytest.mark.slow()),
    pytest.param("ro", marks=pytest.mark.slow()),
    pytest.param("si", marks=pytest.mark.slow()),
    pytest.param("sk", marks=pytest.mark.slow()),
    pytest.param("sl", marks=pytest.mark.slow()),
    pytest.param("sq", marks=pytest.mark.slow()),
    pytest.param("sr", marks=pytest.mark.slow()),
    pytest.param("sv", marks=pytest.mark.slow()),
    pytest.param("ta", marks=pytest.mark.slow()),
    pytest.param("te", marks=pytest.mark.slow()),
    pytest.param("tl", marks=pytest.mark.slow()),
    pytest.param("tr", marks=pytest.mark.slow()),
    pytest.param("tt", marks=pytest.mark.slow()),
    pytest.param("ur", marks=pytest.mark.slow()),
    pytest.param("kmr", marks=pytest.mark.slow()),
]


@pytest.mark.parametrize("lang", LANGUAGES)
def test_tokenizer_explain(lang):
    tokenizer = get_lang_class(lang)().tokenizer
    examples = pytest.importorskip(f"spacy.lang.{lang}.examples")
    for sentence in examples.sentences:
        tokens = [t.text for t in tokenizer(sentence) if not t.is_space]
        debug_tokens = [t[1] for t in tokenizer.explain(sentence)]
        assert tokens == debug_tokens


def test_tokenizer_explain_special_matcher(en_vocab):
    suffix_re = re.compile(r"[\.]$")
    infix_re = re.compile(r"[/]")
    rules = {"a.": [{"ORTH": "a."}]}
    tokenizer = Tokenizer(
        en_vocab,
        rules=rules,
        suffix_search=suffix_re.search,
        infix_finditer=infix_re.finditer,
    )
    tokens = [t.text for t in tokenizer("a/a.")]
    explain_tokens = [t[1] for t in tokenizer.explain("a/a.")]
    assert tokens == explain_tokens


def test_tokenizer_explain_special_matcher_whitespace(en_vocab):
    rules = {":]": [{"ORTH": ":]"}]}
    tokenizer = Tokenizer(
        en_vocab,
        rules=rules,
    )
    text = ": ]"
    tokens = [t.text for t in tokenizer(text)]
    explain_tokens = [t[1] for t in tokenizer.explain(text)]
    assert tokens == explain_tokens


@hypothesis.strategies.composite
def sentence_strategy(draw: hypothesis.strategies.DrawFn, max_n_words: int = 4) -> str:
    """
    Composite strategy for fuzzily generating sentence with varying interpunctation.

    draw (hypothesis.strategies.DrawFn): Protocol for drawing function allowing to fuzzily pick from hypothesis'
                                         strategies.
    max_n_words (int): Max. number of words in generated sentence.
    RETURNS (str): Fuzzily generated sentence.
    """

    punctuation_and_space_regex = "|".join(
        [*[re.escape(p) for p in string.punctuation], r"\s"]
    )
    sentence = [
        [
            draw(hypothesis.strategies.text(min_size=1)),
            draw(hypothesis.strategies.from_regex(punctuation_and_space_regex)),
        ]
        for _ in range(
            draw(hypothesis.strategies.integers(min_value=2, max_value=max_n_words))
        )
    ]

    return " ".join([token for token_pair in sentence for token in token_pair])


@pytest.mark.xfail
@pytest.mark.parametrize("lang", LANGUAGES)
@hypothesis.given(sentence=sentence_strategy())
def test_tokenizer_explain_fuzzy(lang: str, sentence: str) -> None:
    """
    Tests whether output of tokenizer.explain() matches tokenizer output. Input generated by hypothesis.
    lang (str): Language to test.
    text (str): Fuzzily generated sentence to tokenize.
    """

    tokenizer: Tokenizer = spacy.blank(lang).tokenizer
    # Tokenizer.explain is not intended to handle whitespace or control
    # characters in the same way as Tokenizer
    sentence = re.sub(r"\s+", " ", sentence).strip()
    tokens = [t.text for t in tokenizer(sentence)]
    debug_tokens = [t[1] for t in tokenizer.explain(sentence)]
    assert tokens == debug_tokens, f"{tokens}, {debug_tokens}, {sentence}"

import pytest


@pytest.mark.issue(351)
def test_issue351(en_tokenizer):
    doc = en_tokenizer("   This is a cat.")
    assert doc[0].idx == 0
    assert len(doc[0]) == 3
    assert doc[1].idx == 3


@pytest.mark.issue(360)
def test_issue360(en_tokenizer):
    """Test tokenization of big ellipsis"""
    tokens = en_tokenizer("$45...............Asking")
    assert len(tokens) > 2


@pytest.mark.issue(736)
@pytest.mark.parametrize("text,number", [("7am", "7"), ("11p.m.", "11")])
def test_issue736(en_tokenizer, text, number):
    """Test that times like "7am" are tokenized correctly and that numbers are
    converted to string."""
    tokens = en_tokenizer(text)
    assert len(tokens) == 2
    assert tokens[0].text == number


@pytest.mark.issue(740)
@pytest.mark.parametrize("text", ["3/4/2012", "01/12/1900"])
def test_issue740(en_tokenizer, text):
    """Test that dates are not split and kept as one token. This behaviour is
    currently inconsistent, since dates separated by hyphens are still split.
    This will be hard to prevent without causing clashes with numeric ranges."""
    tokens = en_tokenizer(text)
    assert len(tokens) == 1


@pytest.mark.issue(744)
@pytest.mark.parametrize("text", ["We were scared", "We Were Scared"])
def test_issue744(en_tokenizer, text):
    """Test that 'were' and 'Were' are excluded from the contractions
    generated by the English tokenizer exceptions."""
    tokens = en_tokenizer(text)
    assert len(tokens) == 3
    assert tokens[1].text.lower() == "were"


@pytest.mark.issue(759)
@pytest.mark.parametrize(
    "text,is_num", [("one", True), ("ten", True), ("teneleven", False)]
)
def test_issue759(en_tokenizer, text, is_num):
    tokens = en_tokenizer(text)
    assert tokens[0].like_num == is_num


@pytest.mark.issue(775)
@pytest.mark.parametrize("text", ["Shell", "shell", "Shed", "shed"])
def test_issue775(en_tokenizer, text):
    """Test that 'Shell' and 'shell' are excluded from the contractions
    generated by the English tokenizer exceptions."""
    tokens = en_tokenizer(text)
    assert len(tokens) == 1
    assert tokens[0].text == text


@pytest.mark.issue(792)
@pytest.mark.parametrize("text", ["This is a string ", "This is a string\u0020"])
def test_issue792(en_tokenizer, text):
    """Test for Issue #792: Trailing whitespace is removed after tokenization."""
    doc = en_tokenizer(text)
    assert "".join([token.text_with_ws for token in doc]) == text


@pytest.mark.issue(792)
@pytest.mark.parametrize("text", ["This is a string", "This is a string\n"])
def test_control_issue792(en_tokenizer, text):
    """Test base case for Issue #792: Non-trailing whitespace"""
    doc = en_tokenizer(text)
    assert "".join([token.text_with_ws for token in doc]) == text


@pytest.mark.issue(859)
@pytest.mark.parametrize(
    "text", ["aaabbb@ccc.com\nThank you!", "aaabbb@ccc.com \nThank you!"]
)
def test_issue859(en_tokenizer, text):
    """Test that no extra space is added in doc.text method."""
    doc = en_tokenizer(text)
    assert doc.text == text


@pytest.mark.issue(886)
@pytest.mark.parametrize("text", ["Datum:2014-06-02\nDokument:76467"])
def test_issue886(en_tokenizer, text):
    """Test that token.idx matches the original text index for texts with newlines."""
    doc = en_tokenizer(text)
    for token in doc:
        assert len(token.text) == len(token.text_with_ws)
        assert text[token.idx] == token.text[0]


@pytest.mark.issue(891)
@pytest.mark.parametrize("text", ["want/need"])
def test_issue891(en_tokenizer, text):
    """Test that / infixes are split correctly."""
    tokens = en_tokenizer(text)
    assert len(tokens) == 3
    assert tokens[1].text == "/"


@pytest.mark.issue(957)
@pytest.mark.slow
def test_issue957(en_tokenizer):
    """Test that spaCy doesn't hang on many punctuation characters.
    If this test hangs, check (new) regular expressions for conflicting greedy operators
    """
    # Skip test if pytest-timeout is not installed
    pytest.importorskip("pytest_timeout")
    for punct in [".", ",", "'", '"', ":", "?", "!", ";", "-"]:
        string = "0"
        for i in range(1, 100):
            string += punct + str(i)
        doc = en_tokenizer(string)
        assert doc


@pytest.mark.parametrize("text", ["test@example.com", "john.doe@example.co.uk"])
@pytest.mark.issue(1698)
def test_issue1698(en_tokenizer, text):
    """Test that doc doesn't identify email-addresses as URLs"""
    doc = en_tokenizer(text)
    assert len(doc) == 1
    assert not doc[0].like_url


@pytest.mark.issue(1758)
def test_issue1758(en_tokenizer):
    """Test that "would've" is handled by the English tokenizer exceptions."""
    tokens = en_tokenizer("would've")
    assert len(tokens) == 2


@pytest.mark.issue(1773)
def test_issue1773(en_tokenizer):
    """Test that spaces don't receive a POS but no TAG. This is the root cause
    of the serialization issue reported in #1773."""
    doc = en_tokenizer("\n")
    if doc[0].pos_ == "SPACE":
        assert doc[0].tag_ != ""


@pytest.mark.issue(3277)
def test_issue3277(es_tokenizer):
    """Test that hyphens are split correctly as prefixes."""
    doc = es_tokenizer("—Yo me llamo... –murmuró el niño– Emilio Sánchez Pérez.")
    assert len(doc) == 14
    assert doc[0].text == "\u2014"
    assert doc[5].text == "\u2013"
    assert doc[9].text == "\u2013"


@pytest.mark.issue(10699)
@pytest.mark.parametrize("text", ["theses", "thisre"])
def test_issue10699(en_tokenizer, text):
    """Test that 'theses' and 'thisre' are excluded from the contractions
    generated by the English tokenizer exceptions."""
    tokens = en_tokenizer(text)
    assert len(tokens) == 1

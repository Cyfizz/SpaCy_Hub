from typing import cast, Dict, Optional
import pickle
import pytest
from hypothesis import given
import hypothesis.strategies as st
from spacy.pipeline.edit_tree_lemmatizer import EditTreeLemmatizer
from thinc.api import fix_random_seed
from thinc.types import Floats2d
from spacy import util
from spacy.lang.en import English
from spacy.language import Language
from spacy.pipeline._edit_tree_internals.edit_trees import EditTrees
from spacy.training import Example
from spacy.strings import StringStore
from spacy.util import make_tempdir


TRAIN_DATA = [
    ("She likes green eggs", {"lemmas": ["she", "like", "green", "egg"]}),
    ("Eat blue ham", {"lemmas": ["eat", "blue", "ham"]}),
]

PARTIAL_DATA = [
    # partial annotation
    ("She likes green eggs", {"lemmas": ["", "like", "green", ""]}),
    # misaligned partial annotation
    (
        "He hates green eggs",
        {
            "words": ["He", "hat", "es", "green", "eggs"],
            "lemmas": ["", "hat", "e", "green", ""],
        },
    ),
]

LOWERCASING_DATA = [
    ("A B C D", {"lemmas": ["a", "b", "c", "d"]}),
    ("E F G H", {"lemmas": ["e", "f", "g", "h"]}),
    ("I J K L", {"lemmas": ["i", "j", "k", "l"]}),
    ("M N O P", {"lemmas": ["m", "n", "o", "p"]}),
    ("Q R S T", {"lemmas": ["q", "r", "s", "t"]}),
]


@pytest.mark.parametrize("lowercasing", [True, False])
def test_initialize_examples(lowercasing: bool):
    nlp = Language()
    nlp.add_pipe(
        "trainable_lemmatizer",
        config={"model": {"lowercasing": lowercasing}},
    )
    train_examples = []
    for t in TRAIN_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))
    # you shouldn't really call this more than once, but for testing it should be fine
    nlp.initialize(get_examples=lambda: train_examples)
    with pytest.raises(TypeError):
        nlp.initialize(get_examples=lambda: None)  # type:ignore[arg-type, return-value]
    with pytest.raises(TypeError):
        nlp.initialize(get_examples=lambda: train_examples[0])
    with pytest.raises(TypeError):
        nlp.initialize(get_examples=lambda: [])
    with pytest.raises(TypeError):
        nlp.initialize(get_examples=train_examples)  # type:ignore[arg-type]


@pytest.mark.parametrize("lowercasing", [True, False])
def test_initialize_from_labels(lowercasing: bool):
    nlp = Language()
    lemmatizer = cast(
        EditTreeLemmatizer,
        nlp.add_pipe(
            "trainable_lemmatizer",
            config={"model": {"lowercasing": lowercasing}},
        ),
    )
    lemmatizer.min_tree_freq = 1
    train_examples = []
    for t in TRAIN_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))
    nlp.initialize(get_examples=lambda: train_examples)

    nlp2 = Language()
    lemmatizer2 = cast(
        EditTreeLemmatizer,
        nlp2.add_pipe(
            "trainable_lemmatizer",
            config={"model": {"lowercasing": lowercasing}},
        ),
    )
    lemmatizer2.initialize(
        # We want to check that the strings in replacement nodes are
        # added to the string store. Avoid that they get added through
        # the examples.
        get_examples=lambda: train_examples[:1],
        labels=lemmatizer.label_data,
    )

    if lowercasing:
        assert lemmatizer2.tree2label == {2: 1, 0: 0}
        assert lemmatizer2.label_data == {
            "trees": [
                {
                    "prefix_len": 0,
                    "suffix_len": 0,
                    "prefix_tree": 4294967295,
                    "suffix_tree": 4294967295,
                },
                {"orig": "s", "subst": ""},
                {
                    "prefix_len": 0,
                    "suffix_len": 1,
                    "prefix_tree": 4294967295,
                    "suffix_tree": 1,
                },
            ],
            "labels": (0, 2),
        }

    else:
        assert lemmatizer2.tree2label == {1: 0, 3: 1, 4: 2, 6: 3}
        assert lemmatizer2.label_data == {
            "trees": [
                {"orig": "S", "subst": "s"},
                {
                    "prefix_len": 1,
                    "suffix_len": 0,
                    "prefix_tree": 0,
                    "suffix_tree": 4294967295,
                },
                {"orig": "s", "subst": ""},
                {
                    "prefix_len": 0,
                    "suffix_len": 1,
                    "prefix_tree": 4294967295,
                    "suffix_tree": 2,
                },
                {
                    "prefix_len": 0,
                    "suffix_len": 0,
                    "prefix_tree": 4294967295,
                    "suffix_tree": 4294967295,
                },
                {"orig": "E", "subst": "e"},
                {
                    "prefix_len": 1,
                    "suffix_len": 0,
                    "prefix_tree": 5,
                    "suffix_tree": 4294967295,
                },
            ],
            "labels": (1, 3, 4, 6),
        }


@pytest.mark.parametrize("lowercasing", [True, False])
@pytest.mark.parametrize("top_k", (1, 5, 30))
def test_no_data(lowercasing: bool, top_k: int):
    # Test that the lemmatizer provides a nice error when there's no tagging data / labels
    TEXTCAT_DATA = [
        ("I'm so happy.", {"cats": {"POSITIVE": 1.0, "NEGATIVE": 0.0}}),
        ("I'm so angry", {"cats": {"POSITIVE": 0.0, "NEGATIVE": 1.0}}),
    ]
    nlp = English()
    nlp.add_pipe(
        "trainable_lemmatizer",
        config={"model": {"lowercasing": lowercasing}, "top_k": top_k},
    )
    nlp.add_pipe("textcat")

    train_examples = []
    for t in TEXTCAT_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))

    with pytest.raises(ValueError):
        nlp.initialize(get_examples=lambda: train_examples)


@pytest.mark.parametrize("lowercasing", [True, False])
@pytest.mark.parametrize("top_k", (1, 5, 30))
def test_incomplete_data(lowercasing: bool, top_k: int):
    # Test that the lemmatizer works with incomplete information
    nlp = English()
    lemmatizer = cast(
        EditTreeLemmatizer,
        nlp.add_pipe(
            "trainable_lemmatizer",
            config={"model": {"lowercasing": lowercasing}, "top_k": top_k},
        ),
    )
    lemmatizer.min_tree_freq = 1
    fix_random_seed(0)
    train_examples = []
    for t in PARTIAL_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))
    optimizer = nlp.initialize(get_examples=lambda: train_examples)
    for i in range(50):
        losses: Optional[Dict[str, float]] = {}
        nlp.update(train_examples, sgd=optimizer, losses=losses)

    # test the trained model
    test_text = "She likes blue eggs"
    doc = nlp(test_text)
    assert doc[1].lemma_ == "like"
    assert doc[2].lemma_ == "blue"

    # Check that incomplete annotations are ignored.
    scores, _ = lemmatizer.model([eg.predicted for eg in train_examples], is_train=True)
    _, dX = lemmatizer.get_loss(train_examples, scores)
    xp = lemmatizer.model.ops.xp

    # Missing annotations.
    if lowercasing:
        assert xp.count_nonzero(dX[0][0][:-1]) == 0
        assert xp.count_nonzero(dX[0][3][:-1]) == 0
        assert xp.count_nonzero(dX[1][0][:-1]) == 0
        assert xp.count_nonzero(dX[1][3][:-1]) == 0

        # Misaligned annotations.
        assert xp.count_nonzero(dX[1][1][:-1]) == 0

    else:
        assert xp.count_nonzero(dX[0][0]) == 0
        assert xp.count_nonzero(dX[0][3]) == 0
        assert xp.count_nonzero(dX[1][0]) == 0
        assert xp.count_nonzero(dX[1][3]) == 0

        # Misaligned annotations.
        assert xp.count_nonzero(dX[1][1]) == 0


@pytest.mark.parametrize("lowercasing", [True, False])
@pytest.mark.parametrize("top_k", (1, 5, 30))
def test_overfitting_IO(lowercasing: bool, top_k: int):
    nlp = English()
    lemmatizer = cast(
        EditTreeLemmatizer,
        nlp.add_pipe(
            "trainable_lemmatizer",
            config={"model": {"lowercasing": lowercasing}, "top_k": top_k},
        ),
    )
    lemmatizer.min_tree_freq = 1
    fix_random_seed(0)
    train_examples = []
    for t in TRAIN_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))

    optimizer = nlp.initialize(get_examples=lambda: train_examples)

    for i in range(50):
        losses: Optional[Dict[str, float]] = {}
        nlp.update(train_examples, sgd=optimizer, losses=losses)

    test_text = "She likes blue eggs"
    doc = nlp(test_text)
    assert doc[0].lemma_ == "she"
    assert doc[1].lemma_ == "like"
    assert doc[2].lemma_ == "blue"
    assert doc[3].lemma_ == "egg"

    # Check model after a {to,from}_disk roundtrip
    with util.make_tempdir() as tmp_dir:
        nlp.to_disk(tmp_dir)
        nlp2 = util.load_model_from_path(tmp_dir)
        doc2 = nlp2(test_text)
        assert doc2[0].lemma_ == "she"
        assert doc2[1].lemma_ == "like"
        assert doc2[2].lemma_ == "blue"
        assert doc2[3].lemma_ == "egg"

    # Check model after a {to,from}_bytes roundtrip
    nlp_bytes = nlp.to_bytes()
    nlp3 = English()
    nlp3.add_pipe(
        "trainable_lemmatizer",
        config={"model": {"lowercasing": lowercasing}, "top_k": top_k},
    )
    nlp3.from_bytes(nlp_bytes)
    doc3 = nlp3(test_text)
    assert doc3[0].lemma_ == "she"
    assert doc3[1].lemma_ == "like"
    assert doc3[2].lemma_ == "blue"
    assert doc3[3].lemma_ == "egg"

    # Check model after a pickle roundtrip.
    nlp_bytes = pickle.dumps(nlp)
    nlp4 = pickle.loads(nlp_bytes)
    doc4 = nlp4(test_text)
    assert doc4[0].lemma_ == "she"
    assert doc4[1].lemma_ == "like"
    assert doc4[2].lemma_ == "blue"
    assert doc4[3].lemma_ == "egg"


def test_lemmatizer_requires_labels():
    nlp = English()
    nlp.add_pipe("trainable_lemmatizer")
    with pytest.raises(ValueError):
        nlp.initialize()


@pytest.mark.parametrize("lowercasing", [True, False])
def test_lemmatizer_label_data(lowercasing: bool):
    nlp = English()
    lemmatizer = cast(
        EditTreeLemmatizer,
        nlp.add_pipe(
            "trainable_lemmatizer", config={"model": {"lowercasing": lowercasing}}
        ),
    )
    lemmatizer.min_tree_freq = 1
    train_examples = []
    for t in TRAIN_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))

    nlp.initialize(get_examples=lambda: train_examples)
    assert len(lemmatizer.trees) == 3 if lowercasing else 7

    nlp2 = English()
    lemmatizer2 = cast(EditTreeLemmatizer, nlp2.add_pipe("trainable_lemmatizer"))
    lemmatizer2.initialize(
        get_examples=lambda: train_examples, labels=lemmatizer.label_data
    )

    # Verify that the labels and trees are the same.
    assert lemmatizer.labels == lemmatizer2.labels
    assert lemmatizer.trees.to_bytes() == lemmatizer2.trees.to_bytes()


def test_dutch():
    strings = StringStore()
    trees = EditTrees(strings)
    tree = trees.add("deelt", "delen")
    assert trees.tree_to_str(tree) == "(m 0 3 () (m 0 2 (s '' 'l') (s 'lt' 'n')))"

    tree = trees.add("gedeeld", "delen")
    assert (
        trees.tree_to_str(tree) == "(m 2 3 (s 'ge' '') (m 0 2 (s '' 'l') (s 'ld' 'n')))"
    )


def test_from_to_bytes():
    strings = StringStore()
    trees = EditTrees(strings)
    trees.add("deelt", "delen")
    trees.add("gedeeld", "delen")

    b = trees.to_bytes()

    trees2 = EditTrees(strings)
    trees2.from_bytes(b)

    # Verify that the nodes did not change.
    assert len(trees) == len(trees2)
    for i in range(len(trees)):
        assert trees.tree_to_str(i) == trees2.tree_to_str(i)

    # Reinserting the same trees should not add new nodes.
    trees2.add("deelt", "delen")
    trees2.add("gedeeld", "delen")
    assert len(trees) == len(trees2)


def test_from_to_disk():
    strings = StringStore()
    trees = EditTrees(strings)
    trees.add("deelt", "delen")
    trees.add("gedeeld", "delen")

    trees2 = EditTrees(strings)
    with make_tempdir() as temp_dir:
        trees_file = temp_dir / "edit_trees.bin"
        trees.to_disk(trees_file)
        trees2 = trees2.from_disk(trees_file)

    # Verify that the nodes did not change.
    assert len(trees) == len(trees2)
    for i in range(len(trees)):
        assert trees.tree_to_str(i) == trees2.tree_to_str(i)

    # Reinserting the same trees should not add new nodes.
    trees2.add("deelt", "delen")
    trees2.add("gedeeld", "delen")
    assert len(trees) == len(trees2)


@given(st.text(), st.text())
def test_roundtrip(form, lemma):
    strings = StringStore()
    trees = EditTrees(strings)
    tree = trees.add(form, lemma)
    assert trees.apply(tree, form) == lemma


@given(st.text(alphabet="aB"), st.text(alphabet="aB"))
def test_roundtrip_small_alphabet(form, lemma):
    # Test with small alphabets to have more overlap.
    strings = StringStore()
    trees = EditTrees(strings)
    tree = trees.add(form, lemma)
    assert trees.apply(tree, form) == lemma


def test_unapplicable_trees():
    strings = StringStore()
    trees = EditTrees(strings)
    tree3 = trees.add("deelt", "delen")

    # Replacement fails.
    assert trees.apply(tree3, "deeld") == None

    # Suffix + prefix are too large.
    assert trees.apply(tree3, "de") == None


def test_empty_strings():
    strings = StringStore()
    trees = EditTrees(strings)
    no_change = trees.add("xyz", "xyz")
    empty = trees.add("", "")
    assert no_change == empty


@pytest.mark.parametrize("lowercasing", [True, False])
def test_lowercasing(lowercasing: bool):
    nlp = English()
    lemmatizer = cast(
        EditTreeLemmatizer,
        nlp.add_pipe(
            "trainable_lemmatizer", config={"model": {"lowercasing": lowercasing}}
        ),
    )
    lemmatizer.min_tree_freq = 1
    fix_random_seed(0)
    train_examples = []
    for t in LOWERCASING_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))
    optimizer = nlp.initialize(get_examples=lambda: train_examples)
    for _ in range(50):
        losses: Optional[Dict[str, float]] = {}
        nlp.update(train_examples, sgd=optimizer, losses=losses)

    # test the trained model
    test_text = "U V W X"
    doc = nlp(test_text)
    assert doc[0].lemma_ == "u" if lowercasing else "U"
    assert doc[1].lemma_ == "v" if lowercasing else "V"
    assert doc[2].lemma_ == "w" if lowercasing else "W"
    assert doc[3].lemma_ == "x" if lowercasing else "X"
    assert len(lemmatizer.trees) == 1 if lowercasing else 20
    if lowercasing:
        assert lemmatizer.trees.tree_to_str(0) == "(m 0 0 () ())"

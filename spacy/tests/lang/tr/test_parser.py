# coding: utf-8
from __future__ import unicode_literals

from ...util import get_doc


def test_tr_noun_chunks_amod_simple(tr_tokenizer):
    text = "sarı kedi"
    heads = [1, 0]
    deps = ["amod", "ROOT"]
    tags = ["ADJ", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "sarı kedi "


def test_tr_noun_chunks_nmod_simple(tr_tokenizer):
    text = "arkadaşımın kedisi"  # my friend's cat
    heads = [1, 0]
    deps = ["nmod", "ROOT"]
    tags = ["NOUN", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "arkadaşımın kedisi "


def test_tr_noun_chunks_determiner_simple(tr_tokenizer):
    text = "O kedi"  # that cat
    heads = [1, 0]
    deps = ["det", "ROOT"]
    tags = ["DET", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "O kedi "


def test_tr_noun_chunks_nmod_amod(tr_tokenizer):
    text = "okulun eski müdürü"
    heads = [2, 1, 0]
    deps = ["nmod", "amod", "ROOT"]
    tags = ["NOUN", "ADJ", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "okulun eski müdürü "


def test_tr_noun_chunks_one_det_one_adj_simple(tr_tokenizer):
    text = "O sarı kedi"
    heads = [2, 1, 0]
    deps = ["det", "amod", "ROOT"]
    tags = ["DET", "ADJ", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "O sarı kedi "


def test_tr_noun_chunks_two_adjs_simple(tr_tokenizer):
    text = "beyaz tombik kedi"
    heads = [2, 1, 0]
    deps = ["amod", "amod", "ROOT"]
    tags = ["ADJ", "ADJ", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "beyaz tombik kedi "


def test_tr_noun_chunks_one_det_two_adjs_simple(tr_tokenizer):
    text = "o beyaz tombik kedi"
    heads = [3, 2, 1, 0]
    deps = ["det", "amod", "amod", "ROOT"]
    tags = ["DET", "ADJ", "ADJ", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "o beyaz tombik kedi "


def test_tr_noun_chunks_nmod_two(tr_tokenizer):
    text = "kızın saçının rengi"
    heads = [1, 1, 0]
    deps = ["nmod", "nmod", "ROOT"]
    tags = ["NOUN", "NOUN", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "kızın saçının rengi "


def test_tr_noun_chunks_nmod_three(tr_tokenizer):
    text = "güney Afrika ülkelerinden Mozambik"
    heads = [1, 1, 1, 0]
    deps = ["nmod", "nmod", "nmod", "ROOT"]
    tags = ["NOUN", "PROPN", "NOUN", "PROPN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "güney Afrika ülkelerinden Mozambik "


def test_tr_noun_chunks_det_amod_nmod(tr_tokenizer):
    text = "bazı eski oyun kuralları"
    heads = [3, 2, 1, 0]
    deps = ["det", "nmod", "nmod", "ROOT"]
    tags = ["DET", "ADJ", "NOUN", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "bazı eski oyun kuralları "


def test_tr_noun_chunks_acl_simple(tr_tokenizer):
    text = "bahçesi olan okul"
    heads = [2, -1, 0]
    deps = ["acl", "cop", "ROOT"]
    tags = ["NOUN", "AUX", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "bahçesi olan okul "


def test_tr_noun_chunks_acl_verb(tr_tokenizer):
    text = "sevdiğim sanatçılar"
    heads = [1,  0]
    deps = ["acl", "ROOT"]
    tags = ["VERB", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "sevdiğim sanatçılar "


def test_tr_noun_chunks_acl_nmod(tr_tokenizer):
    text = "en sevdiğim ses sanatçısı"
    heads = [1, 2, 1, 0]
    deps = ["advmod", "acl", "nmod", "ROOT"]
    tags = ["ADV", "VERB", "NOUN", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "en sevdiğim ses sanatçısı "


def test_tr_noun_chunks_acl_nmod(tr_tokenizer):
    text = "bildiğim bir turizm şirketi"
    heads = [3, 2, 1, 0]
    deps = ["acl", "det", "nmod", "ROOT"]
    tags = ["VERB", "DET", "NOUN", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "bildiğim bir turizm şirketi "


def test_tr_noun_chunks_np_recursive_nsubj_to_root(tr_tokenizer):
    text = "Simge'nin okuduğu kitap"
    heads = [2, 1, 0]
    deps = ["nsubj", "acl", "ROOT"]
    tags = ["PROPN", "VERB", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "Simge'nin okuduğu kitap "


def test_tr_noun_chunks_np_recursive_nsubj_attached_to_pron_root(tr_tokenizer):
    text = "Simge'nin konuşabileceği birisi"
    heads = [2, 1, 0]
    deps = ["nsubj", "acl", "ROOT"]
    tags = ["PROPN", "VERB", "PRON"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "Simge'nin konuşabileceği birisi "


def test_tr_noun_chunks_np_recursive_nsubj_in_subnp(tr_tokenizer):
    text = "Simge'nin yarın gideceği yer"
    heads = [2, 1, 1, 0]
    deps = ["nsubj", "obl", "acl", "ROOT"]
    tags = ["PROPN", "NOUN", "VERB", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "Simge'nin yarın gideceği yer "


def test_tr_noun_chunks_np_recursive_two_nmods(tr_tokenizer):
    text = "ustanın kapısını degiştireceği çamasır makinası"
    heads = [2, 1, 2, 1, 0]
    deps = ["nsubj", "obj", "acl", "nmod", "ROOT"]
    tags = ["NOUN", "NOUN", "VERB", "NOUN", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "ustanın kapısını degiştireceği çamasır makinası "


def test_tr_noun_chunks_np_recursive_four_nouns(tr_tokenizer):
    text = "kızına piyano dersi verdiğim hanım"
    heads = [3, 1, 1, 1, 0]
    deps = ["obl", "nmod", "obj", "acl", "ROOT"]
    tags = ["NOUN", "NOUN", "NOUN", "VERB", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "kızına piyano dersi verdiğim hanım "

    
def test_tr_noun_chunks_np_recursive_no_nmod(tr_tokenizer):
    text = "içine birkaç çiçek konmuş olan bir vazo"
    heads = [3, 1, 1, 3, -1, 1, 0]
    deps = ["obl", "det", "nsubj", "acl", "aux", "det", "ROOT"]
    tags = ["ADP", "DET", "NOUN", "VERB", "AUX", "DET", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "içine birkaç çiçek konmuş olan bir vazo "


def test_tr_noun_chunks_np_recursive_long_two_acls(tr_tokenizer):
    text = "içine Simge'nin bahçesinden toplanmış birkaç çiçeğin konmuş olduğu bir vazo"
    heads = [6, 1, 1, 2, 1, 1, 3, -1, 1, 0]
    deps = ["obl", "nmod" , "obl", "acl", "det", "nsubj", "acl", "aux", "det", "ROOT"]
    tags = ["ADP", "PROPN", "NOUN", "VERB", "DET", "NOUN", "VERB", "AUX", "DET", "NOUN"]
    tokens = tr_tokenizer(text)
    doc = get_doc(
        tokens.vocab, words=[t.text for t in tokens], tags=tags, heads=heads, deps=deps
    )
    chunks = list(doc.noun_chunks)
    assert len(chunks) == 1
    assert chunks[0].text_with_ws == "içine Simge'nin bahçesinden toplanmış birkaç çiçeğin konmuş olduğu bir vazo "

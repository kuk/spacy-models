import pytest
from spacy.tokens import Doc
from spacy.symbols import SPACE
from pathlib import Path
from ...util import evaluate_corpus


TEST_FILES_DIR = Path(__file__).parent / "test_files"


# TODO: switch back to nkjp when model config is updated
@pytest.mark.parametrize(
    # "test_file,accuracy_threshold",
    # [("nkjp_60s_dev_sample.json", 0.96)],
    "test_file,accuracy_threshold",
    [("pl_sz-ud-dev036_360.json", 0.81)],
)
def test_pl_tagger_corpus(NLP, test_file, accuracy_threshold):
    data_path = TEST_FILES_DIR / test_file
    evaluate_corpus(NLP, data_path, {"tag_acc": accuracy_threshold})


def test_pl_tagger_spaces(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    doc = NLP("Some\nspaces are\tnecessary.")
    assert doc[0].pos != SPACE
    assert doc[0].pos_ != "SPACE"
    assert doc[1].pos == SPACE
    assert doc[1].pos_ == "SPACE"
    assert doc[1].tag_ == "_SP"
    assert doc[2].pos != SPACE
    assert doc[3].pos != SPACE
    assert doc[4].pos == SPACE


def test_pl_tagger_return_char(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    text = (
        "hi Aaron,\r\n\r\nHow is your schedule today, I was wondering if "
        "you had time for a phone\r\ncall this afternoon?\r\n\r\n\r\n"
    )
    doc = NLP(text)
    for token in doc:
        if token.is_space:
            assert token.pos == SPACE
    assert doc[3].text == "\r\n\r\n"
    assert doc[3].is_space
    assert doc[3].pos == SPACE


@pytest.mark.xfail
def test_pl_tagger_lemma_doc(NLP):
    doc = NLP("był", disable=["lemmatizer"])
    doc[0].tag_ = "PRAET"
    lemmatizer = NLP.get_pipe("lemmatizer")
    doc = lemmatizer(doc)
    assert doc[0].lemma_ == "być"


def test_pl_tagger_lemma_assignment(NLP):
    doc = NLP("Poczuł przyjemną woń mocnej kawy.")
    assert all(t.lemma_ != "" for t in doc)

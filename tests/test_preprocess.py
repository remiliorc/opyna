import pandas as pd

from opyna.data.preprocess import clean_text, preprocess


def test_clean_text():
    assert clean_text("  hola\n  mundo ") == "hola mundo"


def test_preprocess_sentiment():
    df = pd.DataFrame({"rating": [1, 3, 5], "title": ["a", "b", "c"],
                       "text": ["x", "y", "z"]})
    out = preprocess(df)
    assert list(out["sentiment"]) == ["negativo", "neutral", "positivo"]

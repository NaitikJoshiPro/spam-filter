import joblib, pathlib, time
from typing import Tuple
import numpy as np

VECT_PATH = 'model/artifacts/vectorizer.joblib'
MODEL_PATH = 'model/artifacts/model.joblib'

_vect = None
_clf = None

def load_model(vectorizer_path=VECT_PATH, model_path=MODEL_PATH):
    global _vect, _clf
    if _vect is None:
        _vect = joblib.load(vectorizer_path)
    if _clf is None:
        _clf = joblib.load(model_path)
    return _vect, _clf

def predict_single(message) -> Tuple[str, float]:
    vect, clf = load_model()
    t0 = time.time()
    x = vect.transform([message])
    probs = None
    if hasattr(clf, 'predict_proba'):
        probs = clf.predict_proba(x)[0]
        # assume classes are in order: clf.classes_
        idx = list(clf.classes_).index('spam') if 'spam' in clf.classes_ else None
        p_spam = probs[idx] if idx is not None else float(max(probs))
    else:
        # use decision_function as proxy
        try:
            df = clf.decision_function(x)
            p_spam = 1.0 / (1.0 + np.exp(-df))[0]
        except Exception:
            p_spam = 0.0
    pred = clf.predict(x)[0]
    latency_ms = (time.time()-t0)*1000
    return pred, float(p_spam), latency_ms

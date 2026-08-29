import math
import itertools
import functools
import sympy
from sympy import Symbol, Rational, Integer

x = Symbol('x')
y = Symbol('y')

def _eval_prop(w, prop_name, default=False):
    try:
        if isinstance(w, dict):
            val = w.get(prop_name, default)
        else:
            val = getattr(w, prop_name, default)
        if callable(val):
            return val()
        return val
    except Exception:
        return default

def conditions(witness) -> list[bool]:
    try:
        is_metric = _eval_prop(witness, 'is_metric_space', False)
        is_tb = _eval_prop(witness, 'is_totally_bounded', False)
        h1_ok = bool(is_metric and is_tb)
    except Exception:
        h1_ok = False

    try:
        comp_is_metric = _eval_prop(witness, 'completion_is_metric_space', is_metric)
        comp_is_compact = _eval_prop(witness, 'completion_is_compact', False)
        q_ok = bool(comp_is_metric and comp_is_compact)
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (X, d) is a totally bounded metric space",
    "¬Q: (\\overline{X}, \\overline{d}) is not a compact metric space"
]

N_HYP = 1
NEG_Q_INDEX = 1
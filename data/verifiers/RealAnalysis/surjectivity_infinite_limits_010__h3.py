import sympy
from sympy import Symbol, S, limit, oo
from sympy.calculus.util import continuous_domain, function_range

x = Symbol('x', real=True)

def conditions(witness):
    try:
        h1 = (continuous_domain(witness, x, S.Reals) == S.Reals)
    except Exception:
        h1 = False

    try:
        h2 = (limit(witness, x, oo) == oo)
    except Exception:
        h2 = False

    try:
        neg_q = (function_range(witness, x, S.Reals) != S.Reals)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is continuous on the entire real line",
    "H_2: The limit of f(x) as x approaches infinity is infinity",
    "¬Q: f is not surjective onto R"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import Symbol, S, limit, oo, solveset, EmptySet
from sympy.calculus.util import continuous_domain, maximum

x = Symbol('x', real=True)

def conditions(witness):
    try:
        dom1 = continuous_domain(witness, x, S.Reals)
        h1 = (dom1 == S.Reals)
    except Exception:
        h1 = False

    try:
        dom2 = continuous_domain(witness, x, S.Reals)
        h2 = (dom2 == S.Reals)
    except Exception:
        h2 = False

    try:
        lim = limit(witness, x, -oo)
        h3 = (lim == -oo)
    except Exception:
        h3 = False

    neg_q = False
    try:
        roots = solveset(witness, x, domain=S.Reals)
        if roots == EmptySet:
            neg_q = True
    except Exception:
        pass

    if not neg_q:
        try:
            max_val = maximum(witness, x, S.Reals)
            if max_val.is_number and max_val.is_real and max_val < 0:
                neg_q = True
        except Exception:
            pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on R",
    "H_2: f is continuous on R",
    "H_3: limit of f(x) as x -> -oo is -oo",
    "¬Q: there is no real number c such that f(c) = 0"
]

N_HYP = 3
NEG_Q_INDEX = 3
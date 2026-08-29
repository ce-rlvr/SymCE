import sympy
from sympy import Symbol, S, limit, oo
from sympy.calculus.util import continuous_domain, function_range

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        witness = sympy.sympify(witness)
    except Exception:
        pass

    # H_1: f is a real-valued function defined on the entire real line R
    # H_2: f is continuous everywhere on R
    try:
        dom = continuous_domain(witness, x, S.Reals)
        h2 = (dom == S.Reals)
    except Exception:
        dom = None
        h2 = False

    try:
        if h2:
            h1 = True
        elif dom is not None:
            undefined_pts = S.Reals - dom
            if isinstance(undefined_pts, sympy.FiniteSet):
                h1 = True
                for pt in undefined_pts:
                    val = witness.subs(x, pt)
                    if val.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan, sympy.I):
                        h1 = False
                        break
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_3: The limit of f(x) as x approaches infinity is infinity
    try:
        lim = limit(witness, x, oo)
        h3 = (lim == oo)
    except Exception:
        h3 = False

    # ¬Q: f does not have a global minimum on R
    try:
        rng = function_range(witness, x, S.Reals)
        neg_q = not bool(rng.contains(rng.inf))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on the entire real line R",
    "H_2: f is continuous everywhere on R",
    "H_3: The limit of f(x) as x approaches infinity is infinity",
    "¬Q: f does not have a global minimum on R"
]

N_HYP = 3
NEG_Q_INDEX = 3
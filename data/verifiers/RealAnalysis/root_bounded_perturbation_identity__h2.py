import sympy
from sympy import Symbol, S, simplify
from sympy.calculus.util import continuous_domain, minimum, maximum
from sympy.solvers.solveset import solveset

x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        if callable(witness):
            g_expr = witness(x)
            f_expr = x + g_expr
        elif isinstance(witness, tuple) and len(witness) == 2:
            g_expr = witness[0](x) if callable(witness[0]) else sympy.sympify(witness[0])
            f_expr = witness[1](x) if callable(witness[1]) else sympy.sympify(witness[1])
        else:
            g_expr = sympy.sympify(witness)
            f_expr = x + g_expr
    except Exception:
        return [False, False, False]

    try:
        dom = continuous_domain(g_expr, x, S.Reals)
        h1 = bool(dom == S.Reals)
    except Exception:
        h1 = False

    try:
        h2 = bool(simplify(f_expr - (x + g_expr)) == 0)
    except Exception:
        h2 = False

    try:
        roots = solveset(f_expr, x, domain=S.Reals)
        if roots == S.EmptySet:
            neg_q = True
        else:
            try:
                min_val = minimum(f_expr, x, S.Reals)
                if min_val > 0:
                    neg_q = True
                else:
                    max_val = maximum(f_expr, x, S.Reals)
                    if max_val < 0:
                        neg_q = True
                    else:
                        neg_q = False
            except Exception:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: g is a continuous function on R",
    "H_2: f(x) = x + g(x) for all x in R",
    "¬Q: There is no c in R such that f(c) = 0"
]

N_HYP = 2
NEG_Q_INDEX = 2
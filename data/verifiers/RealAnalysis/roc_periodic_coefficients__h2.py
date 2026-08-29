import sympy
from sympy import Symbol, limit, oo, Abs, simplify

# Top-level setup
n = Symbol('n', integer=True, positive=True)
x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
    except Exception:
        return [False, False, False]

    # H1: a_n is a sequence of real numbers
    try:
        h1 = True
        for i in range(1, 21):
            val = expr.subs(n, i)
            if val.is_real is False:
                h1 = False
                break
            elif val.is_real is None:
                if val.evalf().is_real is False:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: a_n is not the identically zero sequence
    try:
        h2 = False
        for i in range(1, 21):
            val = expr.subs(n, i)
            if simplify(val) != 0:
                h2 = True
                break
    except Exception:
        h2 = False

    # neg_Q: The radius of convergence is NOT exactly 1
    try:
        R = None
        # Try ratio test
        try:
            ratio = simplify(Abs(expr / expr.subs(n, n + 1)))
            R_ratio = limit(ratio, n, oo)
            if R_ratio.is_number and R_ratio is not sympy.nan:
                R = R_ratio
        except Exception:
            pass

        # Try root test if ratio test didn't give a clear number
        if R is None:
            try:
                root = Abs(expr)**(1/n)
                L = limit(root, n, oo)
                if L == 0:
                    R = oo
                elif L.is_number and L is not sympy.nan:
                    R = 1 / L
            except Exception:
                pass

        neg_q = False
        if R is not None:
            if R != 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a_n is a sequence of real numbers",
    "H_2: a_n is not the identically zero sequence",
    "¬Q: The radius of convergence is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2
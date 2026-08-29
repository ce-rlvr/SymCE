import sympy
from sympy import Symbol, Sum, oo

n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    try:
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
        expr = sympy.sympify(expr)
    except Exception:
        return [False, False]

    try:
        h1 = True
        for i in range(1, 21):
            val = expr.subs(n, i).evalf()
            if not val.is_number:
                h1 = False
                break
            try:
                cval = complex(val)
            except TypeError:
                h1 = False
                break
            if abs(cval.imag) > 1e-12:
                h1 = False
                break
    except Exception:
        h1 = False

    try:
        s = Sum(expr, (n, 1, oo))
        conv = s.is_convergent()
        if conv is False:
            neg_q = True
        elif conv is True:
            neg_q = False
        else:
            val = s.doit()
            if val.has(oo, -oo, sympy.zoo, sympy.nan):
                neg_q = True
            elif val.is_number:
                neg_q = False
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (a_n) is a sequence of real numbers",
    "¬Q: The series does not converge to a real limit"
]

N_HYP = 1
NEG_Q_INDEX = 1
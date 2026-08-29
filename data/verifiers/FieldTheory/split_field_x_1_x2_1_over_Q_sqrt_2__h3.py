import sympy
from sympy import Symbol, sqrt, I, QQ
from sympy.abc import x

Q_sqrt2 = QQ.algebraic_field(sqrt(2))
Q_sqrt2_i = QQ.algebraic_field(sqrt(2), I)
f_poly = (x + 1) * (x**2 + 1)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            f = witness.get('f')
            K = witness.get('K')
            deg = witness.get('deg', witness.get('degree'))
        elif isinstance(witness, tuple) and len(witness) == 4:
            F, f, K, deg = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        if F == Q_sqrt2 or str(F) == str(Q_sqrt2):
            h1 = True
        elif isinstance(F, str) and F.replace(" ", "") in ["Q(sqrt(2))", "QQ(sqrt(2))", "QQ<sqrt(2)>"]:
            h1 = True
        elif isinstance(F, (list, set, tuple)) and set(F) == {sqrt(2)}:
            h1 = True
        elif F == sqrt(2):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(f, str):
            f_expr = sympy.sympify(f)
        elif isinstance(f, sympy.Poly):
            f_expr = f.as_expr()
        else:
            f_expr = f
        h2 = bool(sympy.simplify(f_expr - f_poly) == 0)
    except Exception:
        h2 = False

    try:
        if K == Q_sqrt2_i or str(K) == str(Q_sqrt2_i):
            k_match = True
        elif isinstance(K, str) and K.replace(" ", "") in ["Q(sqrt(2),i)", "QQ(sqrt(2),I)", "QQ<sqrt(2),I>", "Q(sqrt(2),I)"]:
            k_match = True
        elif isinstance(K, (list, set, tuple)) and set(K) == {sqrt(2), I}:
            k_match = True
        elif K == I:
            k_match = True
        else:
            k_match = False
        
        q_holds = k_match and (deg == 2)
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F = Q(sqrt(2))",
    "H_2: f(x) = (x+1)(x^2+1)",
    "¬Q: K != Q(sqrt(2), i) or degree of K over F != 2"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import Symbol, limit, oo, Sum

n = Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    try:
        a_n, b_n = witness
        a_n = sympy.sympify(a_n)
        b_n = sympy.sympify(b_n)
    except Exception:
        return [False, False, False, False]
    
    # H1: (a_n) and (b_n) are sequences of real numbers
    try:
        h1 = True
        for i in range(1, 10):
            val_a = a_n.subs(n, i)
            val_b = b_n.subs(n, i)
            if val_a.is_real is False or val_b.is_real is False:
                h1 = False
                break
            if val_a.is_finite is False or val_b.is_finite is False:
                h1 = False
                break
    except Exception:
        h1 = False

    # H2: (b_n) is a monotonically decreasing sequence
    try:
        h2 = True
        for i in range(1, 100):
            diff = b_n.subs(n, i) - b_n.subs(n, i+1)
            if diff.evalf() < 0:
                h2 = False
                break
    except Exception:
        h2 = False

    # H3: The limit of b_n as n approaches infinity is 0
    try:
        h3 = (limit(b_n, n, oo) == 0)
    except Exception:
        h3 = False

    # ¬Q: The series sum_{n=1}^infty a_n b_n does NOT converge
    try:
        term = a_n * b_n
        s = Sum(term, (n, 1, oo))
        try:
            conv = s.is_convergent()
        except Exception:
            conv = None
            
        if conv is not None:
            neg_q = (conv == False)
        else:
            val = s.doit()
            if isinstance(val, Sum):
                neg_q = False
            elif val.is_finite is False:
                neg_q = True
            else:
                neg_q = val in [oo, -oo, sympy.zoo, sympy.nan]
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (a_n) and (b_n) are sequences of real numbers",
    "H_2: (b_n) is a monotonically decreasing sequence",
    "H_3: The limit of b_n as n approaches infinity is 0",
    "¬Q: The series sum_{n=1}^infty a_n b_n does not converge"
]

N_HYP = 3
NEG_Q_INDEX = 3
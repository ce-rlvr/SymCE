import sympy
from sympy import Sum, oo, Abs, Symbol, limit

n = Symbol('n', integer=True, nonnegative=True)
x = Symbol('x', real=True)

def conditions(witness):
    try:
        a_n, R = witness
        if isinstance(a_n, str):
            a_n = sympy.sympify(a_n)
        else:
            a_n = sympy.sympify(a_n)
            
        if isinstance(R, str):
            R = sympy.sympify(R)
        else:
            R = sympy.sympify(R)
            
        if callable(a_n):
            a_n = a_n(n)
        elif hasattr(a_n, 'free_symbols'):
            syms = list(a_n.free_symbols)
            if len(syms) == 1 and syms[0] != n:
                a_n = a_n.subs(syms[0], n)
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(R > 0 and R < oo)
    except Exception:
        h1 = False

    try:
        try:
            val_0 = a_n.subs(n, 0)
            if val_0.has(sympy.oo, sympy.nan, sympy.zoo):
                start = 1
            else:
                start = 0
        except Exception:
            start = 1

        term = Abs(a_n) * (R**n)
        s = Sum(term, (n, start, oo))
        conv = s.is_convergent()
        
        if conv is not None:
            h2 = bool(conv)
        else:
            ratio = Abs(a_n.subs(n, n+1) / a_n) * R
            L = limit(ratio, n, oo)
            if L < 1:
                h2 = True
            elif L > 1:
                h2 = False
            else:
                root = Abs(a_n)**(1/n) * R
                L2 = limit(root, n, oo)
                if L2 < 1:
                    h2 = True
                else:
                    h2 = False
    except Exception:
        h2 = False

    try:
        neg_q = not h2
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: 0 < R < infinity",
    "H_2: The series sum |a_n| R^n converges",
    "not Q: The power series sum a_n x^n does not converge absolutely for all x in the interval from -R to R"
]

N_HYP = 2
NEG_Q_INDEX = 2
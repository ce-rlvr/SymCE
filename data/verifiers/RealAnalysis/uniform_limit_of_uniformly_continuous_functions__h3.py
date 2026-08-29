import sympy
from sympy import Symbol, S, Interval, oo, limit, Abs
from sympy.calculus.util import maximum
from sympy.sets.sets import Set
from sympy.core.expr import Expr

x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    try:
        domain, f_n, f = witness
        f_n = sympy.sympify(f_n)
        f = sympy.sympify(f)
    except Exception:
        return [False, False, False, False]
        
    # H1: X is a metric space
    try:
        h1 = bool(isinstance(domain, Set))
    except Exception:
        h1 = False
        
    # H2: (f_n) is a sequence of functions from X to R
    try:
        h2 = bool(isinstance(f_n, Expr) and isinstance(f, Expr))
    except Exception:
        h2 = False
        
    # H3: (f_n) converges uniformly to f on X
    try:
        diff = sympy.simplify(f_n - f)
        if diff == 0:
            h3 = True
        elif x not in diff.free_symbols:
            h3 = bool(limit(diff, n, oo) == 0)
        else:
            max_val = maximum(Abs(diff), x, domain)
            h3 = bool(limit(max_val, n, oo) == 0)
    except Exception:
        h3 = False
        
    # neg_Q: f is NOT uniformly continuous on X
    try:
        neg_q = False
        if isinstance(domain, Interval) and domain.measure < oo:
            if domain.left_open:
                L = limit(f, x, domain.start, dir='+')
                if L == oo or L == -oo:
                    neg_q = True
            if domain.right_open:
                L = limit(f, x, domain.end, dir='-')
                if L == oo or L == -oo:
                    neg_q = True
        
        if not neg_q and domain.sup == oo:
            df = f.diff(x)
            L = limit(df, x, oo)
            if L == oo or L == -oo:
                neg_q = True
            else:
                diff_val = limit(f.subs(x, x + 1/x) - f, x, oo)
                if diff_val.is_number and bool(diff_val != 0):
                    neg_q = True

        if not neg_q and domain.inf == -oo:
            df = f.diff(x)
            L = limit(df, x, -oo)
            if L == oo or L == -oo:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: (f_n) is a sequence of functions from X to R",
    "H_3: (f_n) converges uniformly to f on X",
    "¬Q: The limit function f is NOT uniformly continuous on X"
]

N_HYP = 3
NEG_Q_INDEX = 3
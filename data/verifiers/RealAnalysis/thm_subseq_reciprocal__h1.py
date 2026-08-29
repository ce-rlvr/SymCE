import sympy
from sympy.abc import n

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (x, L) where:
      - x is a sympy expression in terms of n (or a callable returning one) representing the sequence x_n.
      - L is a sympy value representing the subsequential limit.
    """
    try:
        x_obj, L = witness
        L = sympy.sympify(L)
        if callable(x_obj):
            x = x_obj(n)
        else:
            x = sympy.sympify(x_obj)
            free_syms = x.free_symbols
            if len(free_syms) == 1:
                sym = list(free_syms)[0]
                x = x.subs(sym, n)
    except Exception:
        return [False, False, False]

    # H1: There exists a real number epsilon > 0 such that |x_n| >= epsilon for all n
    h1 = False
    lim_ok = False
    try:
        lim_abs = sympy.limit(sympy.Abs(x), n, sympy.oo)
        if lim_abs == sympy.oo or (lim_abs.is_real and lim_abs > 0):
            lim_ok = True
    except Exception:
        pass
    
    if not lim_ok:
        try:
            lim_even = sympy.limit(sympy.Abs(x.subs(n, 2*n)), n, sympy.oo)
            lim_odd = sympy.limit(sympy.Abs(x.subs(n, 2*n+1)), n, sympy.oo)
            if (lim_even == sympy.oo or (lim_even.is_real and lim_even > 0)) and \
               (lim_odd == sympy.oo or (lim_odd.is_real and lim_odd > 0)):
                lim_ok = True
        except Exception:
            pass

    if not lim_ok:
        try:
            infimum = sympy.calculus.util.minimum(sympy.Abs(x), n, sympy.Interval(1, sympy.oo))
            if infimum > 0:
                lim_ok = True
        except Exception:
            pass

    if lim_ok:
        min_val = float('inf')
        for i in range(1, 101):
            try:
                val = abs(float(x.subs(n, i).evalf()))
                if val < 1e-9:
                    min_val = 0
                    break
                if val < min_val:
                    min_val = val
            except Exception:
                min_val = 0
                break
        if min_val > 0:
            h1 = True

    # H2: L is a subsequential limit of (x_n)
    h2 = False
    try:
        lim_x = sympy.limit(x, n, sympy.oo)
        if lim_x == L:
            h2 = True
    except Exception:
        pass
        
    if not h2:
        for k in range(2, 5):
            for r in range(k):
                try:
                    lim_sub = sympy.limit(x.subs(n, k*n + r), n, sympy.oo)
                    if lim_sub == L:
                        h2 = True
                        break
                except Exception:
                    pass
            if h2:
                break

    # neg_Q: The real number 1/L is NOT a subsequential limit of (1/x_n)
    # Mathematically, if L is a non-zero real number and a subsequential limit of x_n,
    # then 1/L is ALWAYS a subsequential limit of 1/x_n due to the continuity of f(t)=1/t away from 0.
    # The ONLY way the conclusion fails is if L is not a real number (e.g., L = oo or -oo),
    # making the phrase "The real number 1/L" false, or 1/L undefined as a real number.
    neg_q = False
    try:
        if L.is_real is not True or L == 0:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: There exists a real number epsilon > 0 such that |x_n| >= epsilon for all n",
    "H_2: L is a subsequential limit of (x_n)",
    "not Q: The real number 1/L is not a subsequential limit of (1/x_n) (e.g., L is not real)"
]

N_HYP = 2
NEG_Q_INDEX = 2
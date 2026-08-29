import sympy as sp
from sympy.abc import n

# Top-level setup
# (No specific algebraic structures needed for this real analysis conjecture)

def conditions(witness) -> list[bool]:
    try:
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
    except Exception:
        return [False, False]
        
    # H_1: (x_n) is bounded above
    try:
        h1 = False
        L = sp.limit(expr, n, sp.oo)
        if L == sp.oo:
            h1 = False
        elif type(L).__name__ == 'AccumBounds' and L.max == sp.oo:
            h1 = False
        elif isinstance(L, sp.Limit):
            # Unevaluated limit heuristic
            vals = [sp.re(expr.subs(n, i).evalf()) for i in range(1, 1000)]
            if max(vals) > 1e4:
                h1 = False
            else:
                h1 = True
        else:
            # Check first 100 terms to ensure no oo
            vals = [expr.subs(n, i) for i in range(1, 101)]
            if any(v == sp.oo for v in vals):
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: The limit superior is not a real number or no subsequence converges to it
    try:
        neg_q = False
        L = sp.limit(expr, n, sp.oo)
        if type(L).__name__ == 'AccumBounds':
            limsup = L.max
        else:
            limsup = L
            
        if limsup == sp.oo or limsup == -sp.oo:
            neg_q = True
        elif isinstance(limsup, sp.Limit):
            # Unevaluated limit heuristic
            vals = [sp.re(expr.subs(n, i).evalf()) for i in range(1, 1000)]
            if min(vals) < -1e4 or max(vals) > 1e4:
                neg_q = True
            else:
                neg_q = False
        else:
            # If limsup is finite, check if it's real
            if limsup.is_real is False:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (x_n) is bounded above",
    "¬Q: The limit superior is not a real number or no subsequence converges to it"
]

N_HYP = 1
NEG_Q_INDEX = 1
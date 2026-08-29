import sympy as sp
from sympy.abc import n

# Top-level setup
# (No specific named objects required for Real Analysis sequences)

def conditions(witness) -> list[bool]:
    """
    Given a witness sequence (as a callable or a sympy expression in terms of n),
    evaluates the hypotheses and the negated conclusion.
    """
    try:
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
        expr = sp.sympify(expr)
    except Exception:
        return [False, False, False]

    # H1: (a_n) is monotonically decreasing
    try:
        h1 = True
        for i in range(1, 100):
            term1 = expr.subs(n, i)
            term2 = expr.subs(n, i+1)
            try:
                if not bool(term1 >= term2):
                    h1 = False
                    break
            except TypeError:
                # Expression might have free symbols (sequence of functions) or complex numbers
                free = term1.free_symbols | term2.free_symbols
                is_decreasing = True
                # Test a few points to see if it fails to be decreasing
                for test_val in [1.5, -1.5, 0.0, 3.14]:
                    subs_dict = {sym: test_val for sym in free if sym != n}
                    t1 = term1.subs(subs_dict)
                    t2 = term2.subs(subs_dict)
                    try:
                        if not bool(t1 >= t2):
                            is_decreasing = False
                            break
                    except TypeError:
                        is_decreasing = False
                        break
                if not is_decreasing:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: (a_n) is bounded below
    try:
        h2 = True
        L = sp.limit(expr, n, sp.oo)
        if L == -sp.oo:
            h2 = False
        elif getattr(L, 'is_AccumBounds', False) and L.min == -sp.oo:
            h2 = False
        else:
            # Check first 100 terms just in case it goes to -oo early or contains -oo
            for i in range(1, 100):
                term = expr.subs(n, i)
                try:
                    if bool(term == -sp.oo):
                        h2 = False
                        break
                except TypeError:
                    pass
    except Exception:
        h2 = False

    # neg_Q: The sequence (a_n) does NOT converge to a real number
    try:
        neg_q = False
        L = sp.limit(expr, n, sp.oo)
        if L.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
            neg_q = True
        elif getattr(L, 'is_AccumBounds', False):
            neg_q = True
        elif L.free_symbols:
            # Converges to a function, not a real number
            neg_q = True
        elif L.is_real is False:
            # Converges to a strictly non-real (e.g., complex) number
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (a_n) is monotonically decreasing",
    "H_2: (a_n) is bounded below",
    "¬Q: The sequence (a_n) does not converge to a real number"
]

N_HYP = 2
NEG_Q_INDEX = 2
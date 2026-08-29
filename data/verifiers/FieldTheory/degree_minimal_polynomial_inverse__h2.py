import sympy
from sympy import minpoly, degree, sympify, S
from sympy.abc import x

# Top-level setup for potential witness expressions
QQ = S.Rationals
ZZ = S.Integers

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if it falsifies the conclusion.
    
    The witness can be a dictionary {'alpha': value, 'n': degree},
    a tuple (alpha, n), or just the element alpha (in which case n is inferred).
    """
    try:
        if isinstance(witness, dict):
            alpha = witness.get('alpha', witness.get('a'))
            n = witness.get('n')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            alpha, n = witness
        else:
            alpha = witness
            alpha_sym = sympify(alpha)
            n = degree(minpoly(alpha_sym, x), x)
    except Exception:
        return [False, False, False]

    # H_1: K/F is a field extension
    # We verify this by checking if alpha is an algebraic number (implicitly over F=QQ)
    try:
        alpha_sym = sympify(alpha)
        if not alpha_sym.is_number:
            h1_ok = False
        else:
            mp_alpha = minpoly(alpha_sym, x)
            h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: The minimal polynomial of alpha over F has degree n
    try:
        h2_ok = bool(degree(mp_alpha, x) == n)
    except Exception:
        h2_ok = False

    # ¬Q: alpha^-1 is NOT algebraic over F OR its minimal polynomial does NOT have degree n
    try:
        if alpha_sym == 0:
            # 0^-1 is undefined / not in the field, so it fails the conclusion
            neg_q_ok = True
        else:
            inv_alpha = 1 / alpha_sym
            mp_inv = minpoly(inv_alpha, x)
            deg_inv = degree(mp_inv, x)
            neg_q_ok = bool(deg_inv != n)
    except Exception:
        # If inversion or minpoly computation fails, it is not algebraic
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K/F is a field extension",
    "H_2: The minimal polynomial of alpha over F has degree n",
    "¬Q: alpha^-1 is not algebraic over F or its minimal polynomial does not have degree n"
]

N_HYP = 2
NEG_Q_INDEX = 2
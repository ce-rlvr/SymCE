import sympy
from sympy import symbols, cyclotomic_poly

# Top-level setup
x = symbols('x')

def conditions(witness):
    """
    Given a witness (expected to be a tuple (p, k) or a dict with keys 'p' and 'k'),
    evaluates the hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            k = witness.get('k')
        else:
            p, k = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: k >= 1 is an integer
    try:
        h2 = isinstance(k, (int, sympy.Integer)) and int(k) >= 1
    except Exception:
        h2 = False

    # H_3: N denotes the algebraic norm from Q(zeta_{p^k}) to Q
    # This is a notational definition, so it holds vacuously.
    h3 = True

    # neg_Q: N(1 - zeta_{p^k}) != p
    # The norm of 1 - zeta_n from Q(zeta_n) to Q is exactly the value of the 
    # n-th cyclotomic polynomial evaluated at x = 1.
    try:
        if h1 and h2:
            p_int = int(p)
            k_int = int(k)
            poly = cyclotomic_poly(p_int**k_int, x)
            norm_val = poly.subs(x, 1)
            neg_q = bool(norm_val != p_int)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: k >= 1 is an integer",
    "H_3: N denotes the algebraic norm from Q(zeta_{p^k}) to Q",
    "not Q: N(1 - zeta_{p^k}) != p"
]

N_HYP = 3
NEG_Q_INDEX = 3
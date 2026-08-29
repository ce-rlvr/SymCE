import sympy
from sympy import Symbol, Poly, QQ, GF, ZZ
import math
import itertools
import functools

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Given a witness (K, n, a), checks if it is a valid counterexample to the conjecture.
    K is expected to be a SymPy domain (e.g., QQ, GF(p)).
    """
    try:
        K, n, a = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: K is a field
    try:
        h1_ok = hasattr(K, 'is_Field') and K.is_Field
    except Exception:
        h1_ok = False
        
    # H2: n >= 2 is an integer
    try:
        h2_ok = isinstance(n, int) and n >= 2
    except Exception:
        h2_ok = False
        
    # H3: If 4 divides n, then a not in -4K^4
    try:
        if not (h1_ok and h2_ok):
            h3_ok = False
        elif n % 4 == 0:
            # a in -4K^4 iff 4x^4 + a has a root in K
            poly = Poly(4*x**4 + a, x, domain=K)
            factors = poly.factor_list()[1]
            has_root = any(f.degree() == 1 for f, _ in factors)
            h3_ok = not has_root
        else:
            h3_ok = True
    except Exception:
        h3_ok = False
        
    # neg_Q: x^n - a is NOT irreducible over K
    try:
        if not (h1_ok and h2_ok):
            neg_q_ok = False
        else:
            poly_n = Poly(x**n - a, x, domain=K)
            factors_n = poly_n.factor_list()[1]
            # It is irreducible if there is exactly 1 irreducible factor with multiplicity 1
            is_irreducible = (len(factors_n) == 1 and factors_n[0][1] == 1)
            neg_q_ok = not is_irreducible
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n >= 2 is an integer",
    "H_3: If 4 divides n, then a is not in -4K^4",
    "¬Q: The binomial polynomial x^n - a is reducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3
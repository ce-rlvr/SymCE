import sympy
from sympy.abc import x

# Top-level setup
# (No special named objects required for this number theory / ring theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    try:
        p = int(witness)
        poly = sympy.Poly(x**2 + x + 1, x, modulus=p)
        is_irr = poly.is_irreducible
        p_mod = (p % 3 == 2)
        q = (is_irr == p_mod)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The equivalence (x^2 + x + 1 is irreducible over F_p iff p = 2 mod 3) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1
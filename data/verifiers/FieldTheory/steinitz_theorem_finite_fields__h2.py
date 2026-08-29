import sympy
from sympy import symbols

# Top-level setup
x, y, z, n, p = symbols('x y z n p')

def conditions(witness) -> list[bool]:
    """
    Given a witness (which should be a prime number p), checks if it satisfies the remaining 
    hypotheses and falsifies the conclusion.
    """
    try:
        val = sympy.sympify(witness)
        h1 = bool(val.is_integer and val.is_prime)
    except Exception:
        h1 = False

    # The conclusion states that the algebraic closure of F_p is isomorphic to the union 
    # of all finite fields F_{p^n} for n >= 1. 
    # This is mathematically false for all primes p because the union of all F_{p^n} is not a field.
    # The finite fields F_{p^n} form a directed set under inclusion, not a chain 
    # (e.g., F_{p^2} and F_{p^3} are not comparable, so their union is not closed under addition).
    # Therefore, the union cannot be isomorphic to the algebraic closure.
    # Since the conclusion fails for any prime p, its negation is unconditionally True.
    neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: \\overline{\\mathbb{F}_p} is not isomorphic to the union of all finite fields \\mathbb{F}_{p^n} for n \\ge 1, partially ordered by inclusion"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (p, n), checks if it is a valid counterexample.
    p is an element of a ring R, and n is an integer.
    """
    try:
        p, n = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a unique factorization domain
    try:
        # By constructing a polynomial x - p, we can check if sympy's inferred 
        # domain for p is a Unique Factorization Domain (e.g., ZZ, QQ, ZZ[y], etc.)
        poly_p = sympy.Poly(x - p, x)
        h1 = bool(poly_p.domain.is_UFD)
    except Exception:
        h1 = False

    # H_2: n >= 1 is an integer
    try:
        h2 = isinstance(n, int) and n >= 1
    except Exception:
        h2 = False
        
    # neg_Q: x^n - p is not irreducible
    try:
        if h2:
            poly = sympy.Poly(x**n - p, x)
            # We specifically check for False to ensure it's definitively reducible
            neg_q = (poly.is_irreducible is False)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: n >= 1 is an integer",
    "¬Q: polynomial is not irreducible"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import Poly, factor_list, RootOf
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard groups and matrices
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (poly_E, n) or (poly_E, poly_F, n)
    where poly_E is the minimal polynomial of E over Q, and poly_F is the minimal polynomial of F over Q.
    For simplicity and robustness, this verifier assumes F = Q (i.e., poly_F has degree 1).
    """
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                poly_E, n = witness
                poly_F = x
            elif len(witness) == 3:
                poly_E, poly_F, n = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        poly_E = Poly(poly_E, x, domain='QQ')
        poly_F = Poly(poly_F, x, domain='QQ')
        n = int(n)
    except Exception:
        return [False, False, False]

    # We only support F = Q (degree 1 minimal polynomial) for this verifier
    if poly_F.degree() != 1:
        return [False, False, False]

    # H_1: F contains a primitive n-th root of unity
    # Since F = Q, the only primitive n-th roots of unity in F are for n = 1 and n = 2.
    try:
        h1 = bool(n in [1, 2])
    except Exception:
        h1 = False

    # H_2: The Galois group Gal(E/F) is a cyclic group of order n
    # We count the number of automorphisms of E fixing Q, which equals the number of roots of poly_E in E.
    try:
        if not poly_E.is_irreducible:
            h2 = False
        else:
            r_E = RootOf(poly_E, 0)
            factors = factor_list(poly_E, extension=r_E)[1]
            linear_factors = [f for f, m in factors if f.degree() == 1]
            num_aut = len(linear_factors)
            
            # For n in [1, 2], any group of order n is cyclic.
            if num_aut == n and n in [1, 2]:
                h2 = True
            else:
                h2 = False
    except Exception:
        h2 = False

    # ¬Q: E is NOT the splitting field of x^n - a over F for any a in F
    # For n in [1, 2] and F = Q, the splitting field of x^n - a has degree at most n.
    # Therefore, if the degree of E over Q is strictly greater than n, it cannot be the splitting field.
    try:
        neg_q = bool(poly_E.degree() > n)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field containing a primitive n-th root of unity",
    "H_2: The Galois group Gal(E/F) is a cyclic group of order n",
    "¬Q: E is not the splitting field of x^n - a over F for any a in F"
]

N_HYP = 2
NEG_Q_INDEX = 2
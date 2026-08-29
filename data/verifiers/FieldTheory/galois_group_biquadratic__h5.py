import sympy as sp
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy import eye, zeros

# Top-level setup for potential witness namespace
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    Given a witness (a, b) or (F, a, b), checks if it is a valid counterexample
    to the conjecture. We implicitly evaluate over the field of rational numbers QQ.
    """
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                _, a, b = witness
            elif len(witness) == 2:
                a, b = witness
            else:
                return [False] * 6
        else:
            return [False] * 6
            
        a = sp.sympify(a)
        b = sp.sympify(b)
    except Exception:
        return [False] * 6

    # H_1: F is a field with characteristic not equal to 2
    try:
        # We implicitly work over QQ, which has characteristic 0 != 2.
        h1 = True
    except Exception:
        h1 = False

    # H_2: a and b are elements of F
    try:
        # Check if a and b are rational numbers (elements of QQ)
        h2 = bool(a.is_number and b.is_number and a.is_rational and b.is_rational)
    except Exception:
        h2 = False

    # H_3: There is no element x in F such that x^2 = a
    try:
        # In QQ, this means sqrt(a) is not rational
        h3 = not bool(sp.sqrt(a).is_rational)
    except Exception:
        h3 = False

    # H_4: There is no element y in F such that y^2 = b
    try:
        # In QQ, this means sqrt(b) is not rational
        h4 = not bool(sp.sqrt(b).is_rational)
    except Exception:
        h4 = False

    # H_5: K is the splitting field of the polynomial (x^2 - a)(x^2 - b) over F
    try:
        # This is a definitional hypothesis for K, so it holds by definition.
        h5 = True
    except Exception:
        h5 = False

    # ¬Q: The field extension K/F is not Galois with degree 4, or Gal(K/F) is not V4
    try:
        # Over QQ, the splitting field of (x^2 - a)(x^2 - b) has degree 4 
        # if and only if a, b, and a*b are not squares in QQ.
        # Since H3 and H4 ensure a and b are not squares, the degree is 4 
        # iff a*b is not a square.
        # If a*b is a square, the degree is 2, so the conclusion fails.
        neg_q = bool(sp.sqrt(a * b).is_rational)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field with characteristic not equal to 2",
    "H_2: a and b are elements of F",
    "H_3: There is no element x in F such that x^2 = a",
    "H_4: There is no element y in F such that y^2 = b",
    "H_5: K is the splitting field of the polynomial (x^2 - a)(x^2 - b) over F",
    "¬Q: The field extension K/F is not Galois with degree 4, or Gal(K/F) is not isomorphic to the Klein four-group Z/2Z x Z/2Z"
]

N_HYP = 5
NEG_Q_INDEX = 5
import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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
    # H_1: F is a field
    try:
        h1 = bool(getattr(witness, 'is_Field', False))
    except Exception:
        h1 = False

    # H_2: F^{sep} is the set of all elements in \overline{F} that are separable over F
    # This is a definitional hypothesis establishing the notation F^{sep}.
    h2 = True

    # ¬Q: F^{sep} is not a subfield of \overline{F} or is not separably closed
    # Mathematically, for any field F, its separable closure F^{sep} in the algebraic 
    # closure \overline{F} is unconditionally a subfield and is separably closed.
    # Therefore, the conclusion never fails for any valid field, and its negation is False.
    neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: F^{sep} is the set of all elements in \\overline{F} that are separable over F",
    "¬Q: F^{sep} is not a subfield of \\overline{F} or is not separably closed"
]

N_HYP = 2
NEG_Q_INDEX = 2
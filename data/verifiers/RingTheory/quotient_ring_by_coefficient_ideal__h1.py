import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
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
    h1 = False
    neg_q = False

    # Check H_1: I is an ideal of R
    try:
        if isinstance(witness, dict) and "is_ideal" in witness:
            h1 = bool(witness["is_ideal"])
        elif hasattr(witness, "is_ideal"):
            h1 = bool(witness.is_ideal())
        elif hasattr(witness, "is_ideal_of_R"):
            h1 = bool(witness.is_ideal_of_R())
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if hasattr(I, "is_ideal"):
                h1 = bool(I.is_ideal(R))
            else:
                h1 = True
        else:
            h1 = True
    except Exception:
        h1 = False

    # Check ¬Q: The quotient ring is not isomorphic to the polynomial ring
    try:
        if isinstance(witness, dict) and "neg_q" in witness:
            neg_q = bool(witness["neg_q"])
        elif isinstance(witness, dict) and "is_isomorphic" in witness:
            neg_q = not bool(witness["is_isomorphic"])
        elif hasattr(witness, "is_isomorphic"):
            neg_q = not bool(witness.is_isomorphic())
        elif hasattr(witness, "conclusion_holds"):
            neg_q = not bool(witness.conclusion_holds())
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if hasattr(I, "is_two_sided") and not I.is_two_sided():
                neg_q = True
            elif hasattr(R, "is_commutative") and not R.is_commutative:
                neg_q = True
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "¬Q: The quotient ring is not isomorphic to the polynomial ring"
]

N_HYP = 1
NEG_Q_INDEX = 1
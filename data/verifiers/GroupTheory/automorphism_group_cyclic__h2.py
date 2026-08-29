import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# Representation for the infinite cyclic group
Z = "Z"

def conditions(witness) -> list[bool]:
    # H_1: G is a cyclic group
    h1 = False
    try:
        if witness == "Z" or witness == sympy.S.Integers:
            h1 = True
        elif type(witness).__name__ == 'FreeGroup' and len(witness.generators) == 1:
            h1 = True
        elif type(witness).__name__ == 'FpGroup' and len(witness.generators) == 1 and len(witness.relators) == 0:
            h1 = True
        elif hasattr(witness, 'is_cyclic'):
            val = witness.is_cyclic
            if callable(val):
                h1 = bool(val())
            else:
                h1 = bool(val)
    except Exception:
        h1 = False

    # ¬Q: Aut(G) is NOT isomorphic to (Z/nZ)^x
    # For finite cyclic groups of order n, Aut(G) is always isomorphic to (Z/nZ)^x.
    # The conjecture fails (i.e., ¬Q is True) when G is an infinite cyclic group,
    # because its order n is infinite, making (Z/nZ)^x undefined or not an integer modulo group.
    neg_q = False
    try:
        if witness == "Z" or witness == sympy.S.Integers:
            neg_q = True
        elif type(witness).__name__ == 'FreeGroup' and len(witness.generators) == 1:
            neg_q = True
        elif type(witness).__name__ == 'FpGroup' and len(witness.generators) == 1 and len(witness.relators) == 0:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "¬Q: Aut(G) is not isomorphic to (Z/nZ)^x"
]

N_HYP = 1
NEG_Q_INDEX = 1
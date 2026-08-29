import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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
    # H_1: Let G be a nilpotent group
    try:
        is_nilp = witness.is_nilpotent
        if is_nilp is None:
            h1_ok = False
        else:
            h1_ok = bool(is_nilp)
    except Exception:
        h1_ok = False

    # ¬Q: The quotient group G/Z(G) is NOT torsion-free
    try:
        # For finite groups, G/Z(G) is finite. A finite group is torsion-free 
        # if and only if it is the trivial group.
        # G/Z(G) is the trivial group if and only if G = Z(G), i.e., G is abelian.
        # Therefore, for finite groups, G/Z(G) is not torsion-free iff G is not abelian.
        is_ab = witness.is_abelian
        if is_ab is None:
            neg_q_ok = False
        else:
            neg_q_ok = not bool(is_ab)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: G/Z(G) is not torsion-free"
]

N_HYP = 1
NEG_Q_INDEX = 1
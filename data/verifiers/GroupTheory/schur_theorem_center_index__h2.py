import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    # H_1: G is a group
    try:
        if isinstance(witness, dict) and "is_group" in witness:
            h1 = bool(witness["is_group"])
        elif hasattr(witness, "is_group"):
            h1 = bool(witness.is_group)
        elif isinstance(witness, PermutationGroup):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: The index [G : Z(G)] is finite
    try:
        if isinstance(witness, dict) and "center_index_is_finite" in witness:
            h2 = bool(witness["center_index_is_finite"])
        elif hasattr(witness, "center_index_is_finite"):
            h2 = bool(witness.center_index_is_finite)
        elif isinstance(witness, PermutationGroup):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The commutator subgroup G' is infinite
    try:
        if isinstance(witness, dict) and "derived_subgroup_is_finite" in witness:
            neg_q = not bool(witness["derived_subgroup_is_finite"])
        elif hasattr(witness, "derived_subgroup_is_finite"):
            neg_q = not bool(witness.derived_subgroup_is_finite)
        elif isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: G is a group", "H_2: The index of the center is finite", "¬Q: The commutator subgroup is infinite"]
N_HYP = 2
NEG_Q_INDEX = 2
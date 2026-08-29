import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1 = False
    try:
        if isinstance(witness, dict) and "center_index_finite" in witness:
            h1 = bool(witness["center_index_finite"])
        elif hasattr(witness, "center_index_finite"):
            val = witness.center_index_finite
            h1 = bool(val() if callable(val) else val)
        else:
            if hasattr(witness, "is_finite") and witness.is_finite:
                h1 = True
            else:
                Z = witness.center()
                oG = witness.order()
                oZ = Z.order()
                if oG < oo and oZ < oo:
                    h1 = True
                else:
                    h1 = False
    except Exception:
        h1 = False

    neg_q = False
    try:
        if isinstance(witness, dict) and "derived_subgroup_finite" in witness:
            neg_q = not bool(witness["derived_subgroup_finite"])
        elif hasattr(witness, "derived_subgroup_finite"):
            val = witness.derived_subgroup_finite
            neg_q = not bool(val() if callable(val) else val)
        else:
            D = witness.derived_subgroup()
            if hasattr(D, "is_finite") and D.is_finite is not None:
                neg_q = not D.is_finite
            else:
                oD = D.order()
                neg_q = (oD == oo)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The index of Z(G) in G is finite",
    "not Q: The commutator subgroup is not finite"
]

N_HYP = 1
NEG_Q_INDEX = 1
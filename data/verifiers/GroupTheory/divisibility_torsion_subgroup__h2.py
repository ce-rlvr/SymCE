import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a divisible abelian group",
    "¬Q: T is not a divisible abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        is_abelian = bool(witness.is_abelian)
        if hasattr(witness, "is_divisible"):
            is_divisible = bool(witness.is_divisible)
        else:
            # In the context of finitely generated groups (like SymPy's), 
            # the only divisible abelian group is the trivial group.
            is_divisible = (witness.order() == 1)
        h1 = is_abelian and is_divisible
    except Exception:
        h1 = False

    try:
        if hasattr(witness, "torsion_subgroup"):
            T = witness.torsion_subgroup
            t_is_abelian = bool(T.is_abelian)
            if hasattr(T, "is_divisible"):
                t_is_divisible = bool(T.is_divisible)
            else:
                t_is_divisible = (T.order() == 1)
            q = t_is_abelian and t_is_divisible
        else:
            # For finite groups, all elements are torsion, so T = G
            is_abelian = bool(witness.is_abelian)
            if hasattr(witness, "is_divisible"):
                is_divisible = bool(witness.is_divisible)
            else:
                is_divisible = (witness.order() == 1)
            q = is_abelian and is_divisible
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]
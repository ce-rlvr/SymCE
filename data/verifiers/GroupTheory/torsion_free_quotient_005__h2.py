import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        if getattr(witness, 'is_group', False) and (witness.is_abelian is True):
            if isinstance(witness, PermutationGroup):
                h1 = True
            elif hasattr(witness, 'abelian_invariants'):
                h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        if getattr(witness, 'is_group', False) and (witness.is_abelian is True):
            # By the fundamental theorem of finitely generated abelian groups, 
            # any such group G is isomorphic to Z^r x T, where T is the torsion subgroup.
            # Therefore, the quotient G/T is isomorphic to Z^r, which is ALWAYS a free abelian group.
            # Since G/T is always free abelian for finitely generated abelian groups,
            # the condition "G/T is NOT a free abelian group" is mathematically False.
            is_free_abelian = True
            neg_q = not is_free_abelian
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finitely generated abelian group",
    "¬Q: The quotient group G/T is not a free abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1
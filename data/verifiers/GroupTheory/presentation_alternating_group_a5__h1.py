import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        # The presentation <x, y, z | x^2 = 1, y^3 = 1, z^5 = 1, xyz = 1> 
        # is the standard presentation of the alternating group A_5.
        # A finite group is isomorphic to A_5 iff it has order 60 and is perfect.
        order = witness.order()
        if order == 60:
            derived_order = witness.derived_subgroup().order()
            is_A5 = (derived_order == 60)
        else:
            is_A5 = False
            
        neg_q = not is_A5
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G does not admit the presentation <x, y, z | x^2=1, y^3=1, z^5=1, xyz=1> (i.e. G is not isomorphic to A_5)"
]

N_HYP = 0
NEG_Q_INDEX = 0
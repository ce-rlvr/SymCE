import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            order = witness.order() if callable(witness.order) else witness.order
            if order % 11 != 0:
                # If 11 does not divide the order, the Sylow 11-subgroup is the trivial group,
                # which is unique and normal. Thus the conclusion holds, so neg_q is False.
                neg_q = False
            else:
                P = witness.sylow_subgroup(11)
                is_normal = True
                for g in witness.generators:
                    for h in P.generators:
                        if not P.contains(g * h * ~g):
                            is_normal = False
                            break
                        if not P.contains(~g * h * g):
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G does not have a unique, normal Sylow 11-subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1
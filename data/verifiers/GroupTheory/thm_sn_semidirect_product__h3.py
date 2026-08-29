import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    try:
        n, H = witness
        h1 = (int(n) == n) and (n >= 2)
    except Exception:
        h1 = False

    try:
        n, H = witness
        if not isinstance(H, PermutationGroup):
            h2 = False
        else:
            h2 = True
            for g in H.generators:
                supp = g.support()
                if supp and max(supp) >= n:
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        n, H = witness
        if not isinstance(H, PermutationGroup):
            neg_q = False
        else:
            is_subgroup = True
            for g in H.generators:
                supp = g.support()
                if supp and max(supp) >= n:
                    is_subgroup = False
                    break
            
            if not is_subgroup:
                neg_q = True
            elif H.order() != 2:
                neg_q = True
            else:
                is_semidirect = True
                for g in H.generators:
                    if not g.is_Identity and g.is_even:
                        is_semidirect = False
                        break
                neg_q = not is_semidirect
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 2",
    "H_2: H is a subgroup of S_n",
    "¬Q: S_n is not the internal semidirect product of A_n and H"
]

N_HYP = 2
NEG_Q_INDEX = 2
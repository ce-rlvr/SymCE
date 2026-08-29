import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
    # H_1: G is a finite group
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: G is not the trivial group
    try:
        h2_ok = h1_ok and (witness.order() > 1)
    except Exception:
        h2_ok = False

    # ¬Q: G does not contain a non-trivial abelian normal subgroup
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            has_abelian_normal = False
            elements = list(witness.elements)
            for x in elements:
                if x.is_Identity:
                    continue
                
                try:
                    H = PermutationGroup([x])
                    NC = witness.normal_closure(H)
                except Exception:
                    try:
                        NC = witness.normal_closure([x])
                    except Exception:
                        conjugates = set()
                        for g in elements:
                            conjugates.add(g * x * ~g)
                        NC = PermutationGroup(list(conjugates))
                        
                if NC.is_abelian:
                    has_abelian_normal = True
                    break
            neg_q_ok = not has_abelian_normal
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is not the trivial group",
    "¬Q: G does not contain a non-trivial abelian normal subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness) -> list[bool]:
    try:
        witness_list = list(witness)
    except Exception:
        return [False, False]

    try:
        perms = []
        for p in witness_list:
            if not isinstance(p, Permutation):
                p = Permutation(p)
            perms.append(p)
            
        if not perms:
            h1 = False
        else:
            h1 = any(not p.is_even for p in perms)
    except Exception:
        h1 = False

    try:
        perms = []
        for p in witness_list:
            if not isinstance(p, Permutation):
                p = Permutation(p)
            perms.append(p)
            
        if not perms:
            neg_q = False
        else:
            even_count = sum(1 for p in perms if p.is_even)
            odd_count = sum(1 for p in perms if not p.is_even)
            neg_q = (even_count != odd_count)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H contains at least one odd permutation",
    "¬Q: H does not have exactly half even and half odd permutations"
]

N_HYP = 1
NEG_Q_INDEX = 1
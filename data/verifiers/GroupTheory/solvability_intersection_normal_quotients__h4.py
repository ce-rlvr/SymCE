import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H and K are normal subgroups of G
    try:
        def is_normal(grp, subgrp):
            if not subgrp.is_subgroup(grp):
                return False
            for g in grp.generators:
                g_inv = ~g
                for h in subgrp.generators:
                    if (g * h * g_inv) not in subgrp:
                        return False
            return True
        
        h2 = is_normal(G, H) and is_normal(G, K)
    except Exception:
        h2 = False

    # H_3: The quotient group G/H is solvable
    try:
        def is_quotient_solvable(grp, subgrp):
            # G/H is solvable iff the derived series of G eventually lands in H
            curr = grp
            while True:
                if curr.is_subgroup(subgrp):
                    return True
                next_curr = curr.derived_subgroup()
                if next_curr.order() == curr.order():
                    return False
                curr = next_curr
                
        h3 = is_quotient_solvable(G, H)
    except Exception:
        h3 = False

    # neg_Q: The quotient group G/(H \cap K) is NOT solvable
    try:
        def is_intersection_quotient_solvable(grp, sub1, sub2):
            # G/(H \cap K) is solvable iff the derived series of G eventually lands in H \cap K.
            # This is equivalent to the derived series eventually landing in both H and K.
            curr = grp
            while True:
                if curr.is_subgroup(sub1) and curr.is_subgroup(sub2):
                    return True
                next_curr = curr.derived_subgroup()
                if next_curr.order() == curr.order():
                    return False
                curr = next_curr
                
        neg_q = not is_intersection_quotient_solvable(G, H, K)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H and K are normal subgroups of G",
    "H_3: The quotient group G/H is solvable",
    "¬Q: The quotient group G/(H \cap K) is not solvable"
]

N_HYP = 3
NEG_Q_INDEX = 3
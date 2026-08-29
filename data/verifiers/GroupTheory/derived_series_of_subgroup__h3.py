import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        if len(witness) == 3:
            G, H, n = witness
        elif len(witness) == 2:
            G, H = witness
            n = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            h2 = all(g in G for g in H.generators)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        neg_q = False
        def is_sub(sub, super_grp):
            return all(g in super_grp for g in sub.generators)

        if len(witness) == 3:
            if isinstance(n, int) and n >= 0:
                curr_G = G
                curr_H = H
                for _ in range(n):
                    curr_G = curr_G.derived_subgroup()
                    curr_H = curr_H.derived_subgroup()
                neg_q = not is_sub(curr_H, curr_G)
        elif len(witness) == 2:
            curr_G = G
            curr_H = H
            if not is_sub(curr_H, curr_G):
                neg_q = True
            else:
                while True:
                    next_G = curr_G.derived_subgroup()
                    next_H = curr_H.derived_subgroup()
                    if not is_sub(next_H, next_G):
                        neg_q = True
                        break
                    if next_G.order() == curr_G.order() and next_H.order() == curr_H.order():
                        break
                    curr_G = next_G
                    curr_H = next_H
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: The n-th derived subgroup H^(n) is not a subgroup of the n-th derived subgroup G^(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2
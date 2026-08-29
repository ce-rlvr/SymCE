import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
        if len(witness) != 3:
            return [False, False, False, False]
        G, H, alpha = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: H is a subgroup of G
    try:
        h2_ok = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2_ok = False

    # H_3: The index of H in G, denoted [G : H], is a finite integer n
    try:
        if h1_ok and h2_ok:
            n = G.order() // H.order()
            h3_ok = (G.order() % H.order() == 0)
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # neg_Q: The index of the image subgroup [G : \alpha(H)] is not equal to n
    try:
        if isinstance(alpha, dict):
            image_elements = {alpha.get(g, g) for g in H.elements}
        elif callable(alpha):
            image_elements = {alpha(g) for g in H.elements}
        else:
            image_elements = {alpha * g * (~alpha) for g in H.elements}
        
        is_subgroup = True
        if not image_elements:
            is_subgroup = False
        else:
            for a in image_elements:
                for b in image_elements:
                    if (a * b) not in image_elements:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
        
        if not is_subgroup:
            neg_q_ok = True
        else:
            alpha_H = PermutationGroup(list(image_elements))
            if not alpha_H.is_subgroup(G):
                neg_q_ok = True
            else:
                index_alpha_H = G.order() // alpha_H.order()
                neg_q_ok = (index_alpha_H != n)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: G is a group", "H_2: H is a subgroup of G", "H_3: The index of H in G is a finite integer n", "¬Q: The index of the image subgroup is not equal to n"]
N_HYP = 3
NEG_Q_INDEX = 3
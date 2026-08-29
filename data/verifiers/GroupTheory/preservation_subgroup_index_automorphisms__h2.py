import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    "H_1: G is a group",
    "H_2: The index of H in G is a finite integer n",
    "H_3: alpha is an automorphism of G",
    "¬Q: The index of the image subgroup is not equal to n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, H, alpha = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The index of H in G is a finite integer n
    h2 = False
    n = None
    try:
        if h1:
            if isinstance(H, PermutationGroup):
                if all(g in G for g in H.generators):
                    if G.order() % H.order() == 0:
                        h2 = True
                        n = G.order() // H.order()
            elif isinstance(H, (list, tuple, set)):
                H_list = list(set(H))
                if len(H_list) > 0 and all(h in G for h in H_list):
                    is_sub = True
                    for h1_el in H_list:
                        for h2_el in H_list:
                            if h1_el * h2_el not in H_list:
                                is_sub = False
                                break
                        if not is_sub:
                            break
                    if is_sub and G.order() % len(H_list) == 0:
                        h2 = True
                        n = G.order() // len(H_list)
    except Exception:
        h2 = False

    # H_3: alpha is an automorphism of G
    h3 = False
    alpha_map = {}
    try:
        if h1:
            elements = list(G.generate())
            if isinstance(alpha, dict):
                alpha_map = alpha
            elif callable(alpha):
                for g in elements:
                    alpha_map[g] = alpha(g)
            
            if len(alpha_map) == len(elements) and set(alpha_map.keys()) == set(elements) and set(alpha_map.values()) == set(elements):
                is_hom = True
                for g1 in elements:
                    for g2 in elements:
                        if alpha_map[g1 * g2] != alpha_map[g1] * alpha_map[g2]:
                            is_hom = False
                            break
                    if not is_hom:
                        break
                if is_hom:
                    h3 = True
    except Exception:
        h3 = False

    # ¬Q: The index of the image subgroup is not equal to n
    neg_q = False
    try:
        if h1 and h2 and h3:
            if isinstance(H, PermutationGroup):
                img_elements = [alpha_map[g] for g in H.generators]
                if not img_elements:
                    img_elements = [list(G.generate())[0]**0]
                img_H = PermutationGroup(*img_elements)
                if G.order() % img_H.order() == 0:
                    img_index = G.order() // img_H.order()
                    neg_q = (img_index != n)
                else:
                    neg_q = True
            elif isinstance(H, (list, tuple, set)):
                H_list = list(set(H))
                img_elements = [alpha_map[g] for g in H_list]
                if not img_elements:
                    img_elements = [list(G.generate())[0]**0]
                img_H = PermutationGroup(*img_elements)
                if G.order() % img_H.order() == 0:
                    img_index = G.order() // img_H.order()
                    neg_q = (img_index != n)
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]
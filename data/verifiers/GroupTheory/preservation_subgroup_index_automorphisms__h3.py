import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.abc
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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
    "H_2: H is a subgroup of G",
    "H_3: alpha is an automorphism of G",
    "¬Q: The index of the image subgroup alpha(H) in G is not equal to n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, H, alpha, n = witness
        elif len(witness) == 3:
            G, H, alpha = witness
            n = (G.order() // H.order()) + 1
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: H is a subgroup of G
    try:
        h2_ok = isinstance(H, PermutationGroup) and all(g in G for g in H.generators)
    except Exception:
        h2_ok = False
        
    # H_3: alpha is an automorphism of G
    try:
        elements = list(G.elements)
        if isinstance(alpha, dict):
            mapping = alpha
        else:
            mapping = {g: alpha(g) for g in elements}
            
        is_bijection = (set(mapping.keys()) == set(elements)) and (set(mapping.values()) == set(elements))
        is_homomorphism = True
        if is_bijection:
            for g1 in elements:
                for g2 in elements:
                    if mapping[g1 * g2] != mapping[g1] * mapping[g2]:
                        is_homomorphism = False
                        break
                if not is_homomorphism:
                    break
        h3_ok = is_bijection and is_homomorphism
    except Exception:
        h3_ok = False
        
    # neg_Q: index of alpha(H) in G != n
    try:
        alpha_H_elements = [mapping[h] for h in list(H.elements)]
        alpha_H = PermutationGroup(alpha_H_elements)
        index = G.order() // alpha_H.order()
        neg_q_ok = (index != n)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]
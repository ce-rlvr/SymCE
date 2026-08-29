import itertools
import math
import functools

import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    "H_2: H is a characteristic subgroup of G",
    "H_3: Aut(G) is the automorphism group of G",
    "¬Q: The subgroup H is not a fixed point under the action of Aut(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) >= 2:
                G = witness[0]
                H = witness[1]
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    is_char = False
    auts_computed = False
    try:
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup) and H.is_subgroup(G):
            gens = G.generators
            elements = list(G.generate())
            auts = []
            
            id_G = G.identity
            G_order = G.order()
            
            for images in itertools.product(elements, repeat=len(gens)):
                mapping = {}
                mapping[id_G] = id_G
                queue = [id_G]
                valid = True
                
                head = 0
                while head < len(queue) and valid:
                    curr = queue[head]
                    head += 1
                    curr_img = mapping[curr]
                    
                    for g, img_g in zip(gens, images):
                        nxt = curr * g
                        nxt_img = curr_img * img_g
                        
                        if nxt in mapping:
                            if mapping[nxt] != nxt_img:
                                valid = False
                                break
                        else:
                            mapping[nxt] = nxt_img
                            queue.append(nxt)
                            
                if valid and len(set(mapping.values())) == G_order:
                    auts.append(mapping)
                    
            is_char_temp = True
            H_elements = set(H.generate())
            for mapping in auts:
                for x in H.generators:
                    if x not in mapping:
                        is_char_temp = False
                        break
                    img = mapping[x]
                    if img not in H_elements:
                        is_char_temp = False
                        break
                if not is_char_temp:
                    break
            is_char = is_char_temp
            auts_computed = True
    except Exception:
        pass

    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        h2_ok = auts_computed and is_char
    except Exception:
        h2_ok = False

    try:
        h3_ok = h1_ok
    except Exception:
        h3_ok = False

    try:
        neg_q_ok = auts_computed and not is_char
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]
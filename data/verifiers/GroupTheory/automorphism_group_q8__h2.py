import math
import itertools
import functools
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

def is_automorphism_group_S4(G):
    try:
        elements = []
        for i, e in enumerate(G.generate()):
            if i >= 3000:
                # If the group is this large, its automorphism group cannot be S4
                # (since |Aut(G)| <= 24 implies |G| <= 2160)
                return False
            elements.append(e)
        n = len(elements)
    except Exception:
        return False
        
    if n == 1:
        return False
        
    try:
        gens = G.generators
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        mult_table = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                mult_table[i][j] = elem_to_idx[elements[i] * elements[j]]
                
        gen_indices = [elem_to_idx[g] for g in gens]
        
        id_idx = None
        for i in range(n):
            if mult_table[i][i] == i:
                id_idx = i
                break
        if id_idx is None:
            return False
    except Exception:
        return False
        
    automorphisms = []
    
    try:
        for image_tuple in itertools.product(range(n), repeat=len(gen_indices)):
            proposed_images = dict(zip(gen_indices, image_tuple))
            
            mapping = {id_idx: id_idx}
            valid = True
            discovered = [id_idx]
            
            head = 0
            while head < len(discovered) and valid:
                curr = discovered[head]
                head += 1
                
                for g_idx in gen_indices:
                    nxt = mult_table[curr][g_idx]
                    nxt_img = mult_table[mapping[curr]][proposed_images[g_idx]]
                    
                    if nxt in mapping:
                        if mapping[nxt] != nxt_img:
                            valid = False
                            break
                    else:
                        mapping[nxt] = nxt_img
                        discovered.append(nxt)
                        
            if valid and len(set(mapping.values())) == n:
                aut_map = tuple(mapping[i] for i in range(n))
                automorphisms.append(aut_map)
                if len(automorphisms) > 24:
                    return False
    except Exception:
        return False
                
    if len(automorphisms) != 24:
        return False
        
    try:
        # S4 is uniquely determined among groups of order 24 by its order profile
        orders = {}
        for aut_map in automorphisms:
            p = Permutation(list(aut_map))
            o = p.order()
            orders[o] = orders.get(o, 0) + 1
            
        expected_orders = {1: 1, 2: 9, 3: 8, 4: 6}
        return orders == expected_orders
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        if h1:
            neg_q = not is_automorphism_group_S4(witness)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The automorphism group of G is not isomorphic to S_4"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
import itertools
import functools
import math

# Top-level setup for witness expressions
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

def is_characteristic(H, K):
    """
    Checks if K is a characteristic subgroup of H.
    A subgroup is characteristic if it is invariant under all automorphisms of H.
    """
    if not isinstance(H, PermutationGroup) or not isinstance(K, PermutationGroup):
        return False
    if not K.is_subgroup(H):
        return False
        
    # Limit order to prevent timeouts on excessively large groups
    if H.order() > 256:
        return False
        
    elements = list(H.generate())
    if not elements:
        return False
        
    id_elem = elements[0]**0
    n = len(elements)
    gens = H.generators
    
    K_elements = set(K.generate())
    
    # Find all automorphisms by mapping generators to all possible tuples of elements
    for target_gens in itertools.product(elements, repeat=len(gens)):
        f = {id_elem: id_elem}
        queue = [id_elem]
        head = 0
        valid = True
        
        # Build the homomorphism using BFS
        while head < len(queue):
            curr = queue[head]
            head += 1
            for i, g in enumerate(gens):
                nxt = curr * g
                nxt_val = f[curr] * target_gens[i]
                if nxt in f:
                    if f[nxt] != nxt_val:
                        valid = False
                        break
                else:
                    f[nxt] = nxt_val
                    queue.append(nxt)
            if not valid:
                break
                
        if not valid:
            continue
            
        # Check if the homomorphism is a bijection (hence an automorphism)
        if len(set(f.values())) != n:
            continue
            
        # Check if K is invariant under this automorphism
        k_invariant = True
        for k in K_elements:
            if f[k] not in K_elements:
                k_invariant = False
                break
                
        if not k_invariant:
            return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]
        
    # H_1: Let G be a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: Let K be a characteristic subgroup of H
    try:
        h2 = is_characteristic(H, K)
    except Exception:
        h2 = False
        
    # ¬Q: K is not a characteristic subgroup of G
    try:
        neg_q = not is_characteristic(G, K)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a characteristic subgroup of H",
    "¬Q: K is not a characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2
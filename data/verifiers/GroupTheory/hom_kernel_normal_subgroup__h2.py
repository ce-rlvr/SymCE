import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import itertools
import functools
import math

# Top-level setup: named object bindings for witness expressions
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

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False]
        
    # Convert list of pairs to dict if necessary
    if isinstance(phi, (list, tuple)) and all(isinstance(item, (list, tuple)) and len(item) == 2 for item in phi):
        try:
            phi = dict(phi)
        except Exception:
            pass

    # H_1: G and H are groups, and phi is a well-defined map from G to H
    try:
        h1 = False
        if hasattr(G, 'elements') and hasattr(H, 'elements'):
            G_els = list(G.elements)
            H_els = list(H.elements)
            
            if isinstance(phi, dict):
                if all(g in phi for g in G_els) and all(phi[g] in H_els for g in G_els):
                    h1 = True
            elif callable(phi):
                if all(phi(g) in H_els for g in G_els):
                    h1 = True
    except Exception:
        h1 = False

    # neg_Q: ker(phi) is NOT a normal subgroup of G
    try:
        G_els = list(G.elements)
        
        # Find the identity elements of H and G
        H_id = None
        for h in H.elements:
            H_id = h * (h**-1)
            break
            
        G_id = None
        for g in G.elements:
            G_id = g * (g**-1)
            break
            
        # Construct the kernel
        if isinstance(phi, dict):
            K = {g for g in G_els if phi.get(g) == H_id}
        else:
            K = {g for g in G_els if phi(g) == H_id}
            
        # Check if K is a subgroup
        is_subgroup = True
        if G_id not in K:
            is_subgroup = False
        else:
            for a in K:
                for b in K:
                    if a * b not in K:
                        is_subgroup = False
                        break
                if a**-1 not in K:
                    is_subgroup = False
                if not is_subgroup:
                    break
                    
        # Check if K is normal in G
        is_normal = True
        if is_subgroup:
            for g in G_els:
                for k in K:
                    if g * k * (g**-1) not in K:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
        is_normal_subgroup = is_subgroup and is_normal
        neg_q = not is_normal_subgroup
        
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups and phi is a map from G to H",
    "¬Q: ker(phi) is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        if h1:
            G_elems = list(G.elements)
            H_elems = list(H.elements)
            if isinstance(phi, dict):
                h2 = all(g in phi for g in G_elems) and all(phi[g] in H_elems for g in G_elems)
            elif callable(phi):
                h2 = True
                phi_dict = {}
                for g in G_elems:
                    try:
                        val = phi(g)
                        if val not in H_elems:
                            h2 = False
                            break
                        phi_dict[g] = val
                    except Exception:
                        h2 = False
                        break
                if h2:
                    phi = phi_dict
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            G_prime = G.derived_subgroup()
            H_prime = H.derived_subgroup()
            
            H_prime_elems = set(H_prime.elements)
            preimage = {g for g in G_elems if phi[g] in H_prime_elems}
            
            id_G = None
            for g in G_elems:
                if g * g == g:
                    id_G = g
                    break
                    
            is_subgroup = True
            if id_G not in preimage:
                is_subgroup = False
            else:
                for a in preimage:
                    if a**-1 not in preimage:
                        is_subgroup = False
                        break
                    for b in preimage:
                        if a * b not in preimage:
                            is_subgroup = False
                            break
                            
            is_normal = True
            if is_subgroup:
                for g in G_elems:
                    g_inv = g**-1
                    for n in preimage:
                        if g * n * g_inv not in preimage:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                        
            contains_G_prime = True
            for c in G_prime.elements:
                if c not in preimage:
                    contains_G_prime = False
                    break
                    
            neg_q = not (is_subgroup and is_normal and contains_G_prime)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: derived subgroups are defined",
    "¬Q: preimage of H derived subgroup is not normal or lacks G derived subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2
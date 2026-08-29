import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False]
    
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # ¬Q: The kernel of phi is not a normal subgroup of G
    try:
        if not h1:
            neg_q = False
        else:
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            
            # Find the identity element of H
            H_id = None
            for h in H_elements:
                if h * h == h:
                    H_id = h
                    break
            
            if H_id is None:
                neg_q = False
            else:
                # Compute the kernel of phi
                ker = set()
                for g in G_elements:
                    if isinstance(phi, dict):
                        val = phi[g]
                    elif callable(phi):
                        val = phi(g)
                    else:
                        val = dict(phi)[g]
                    
                    if val == H_id:
                        ker.add(g)
                
                # Check if ker is a subgroup
                is_subgroup = True
                if not ker:
                    is_subgroup = False
                else:
                    for a in ker:
                        if ~a not in ker:
                            is_subgroup = False
                            break
                        for b in ker:
                            if a * b not in ker:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                
                # Check if ker is normal in G
                is_normal = True
                if is_subgroup:
                    for g in G_elements:
                        for k in ker:
                            if g * k * ~g not in ker:
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
    "H_1: G and H are groups",
    "¬Q: The kernel of phi is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1
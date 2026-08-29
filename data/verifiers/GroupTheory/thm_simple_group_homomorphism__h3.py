import sympy
from sympy.combinatorics import PermutationGroup
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

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, H, phi = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
        if h1:
            _ = G.identity
            _ = H.identity
    except Exception:
        h1 = False

    # H2: G is a simple group
    try:
        normals = G.normal_subgroups()
        h2 = (len(normals) == 2)
    except Exception:
        h2 = False

    # H3: phi is not the trivial homomorphism
    try:
        H_elems = set(H.elements)
        G_elems = list(G.elements)
        is_trivial = True
        for g in G_elems:
            if isinstance(phi, dict):
                val = phi[g]
            else:
                val = phi(g)
            if val not in H_elems:
                raise ValueError("Mapped value not in H")
            if val != H.identity:
                is_trivial = False
                break
        h3 = not is_trivial
    except Exception:
        h3 = False

    # neg_Q: not (phi is injective and G isomorphic to phi(G))
    try:
        H_elems = set(H.elements)
        G_elems = list(G.elements)
        mapped_elements = set()
        for g in G_elems:
            if isinstance(phi, dict):
                val = phi[g]
            else:
                val = phi(g)
            if val not in H_elems:
                raise ValueError("Mapped value not in H")
            mapped_elements.add(val)
        
        is_injective = (len(mapped_elements) == len(G_elems))
        
        if not is_injective:
            neg_q = True
        else:
            H_id = H.identity
            if H_id not in mapped_elements:
                is_subgroup = False
            else:
                is_subgroup = True
                for a in mapped_elements:
                    for b in mapped_elements:
                        if (a * b) not in mapped_elements:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
            
            if not is_subgroup:
                neg_q = True
            else:
                phi_G = PermutationGroup(*list(mapped_elements))
                try:
                    is_iso = G.is_isomorphic(phi_G)
                except Exception:
                    # Fallback if is_isomorphic is unavailable:
                    # Since G is simple and phi is injective, phi_G has the same order.
                    # For small groups, they are isomorphic iff phi_G is also simple.
                    is_iso = (len(phi_G.normal_subgroups()) == 2)
                neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G is a simple group",
    "H_3: ϕ is not the trivial homomorphism",
    "¬Q: ϕ is not injective or G is not isomorphic to ϕ(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3
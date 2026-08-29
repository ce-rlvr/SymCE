import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def get_phi_func(phi):
    if isinstance(phi, dict):
        return lambda x: phi.get(x, None)
    elif callable(phi):
        return phi
    elif hasattr(phi, 'apply'):
        return phi.apply
    elif hasattr(phi, 'image'):
        return phi.image
    else:
        return None

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = bool(hasattr(G, 'elements') and hasattr(H, 'elements') and 
                  hasattr(G, 'derived_subgroup') and hasattr(H, 'derived_subgroup'))
    except Exception:
        h1 = False

    # H_2: phi: G -> H is a group homomorphism
    try:
        h2 = True
        phi_func = get_phi_func(phi)
        if phi_func is None:
            h2 = False
        else:
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            for x in G_elements:
                if phi_func(x) not in H_elements:
                    h2 = False
                    break
            if h2:
                for x in G_elements:
                    for y in G_elements:
                        if phi_func(x * y) != phi_func(x) * phi_func(y):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # ¬Q: The preimage of the derived subgroup of H is not a normal subgroup of G or does not contain the derived subgroup of G
    try:
        phi_func = get_phi_func(phi)
        if phi_func is None:
            neg_Q = False
        else:
            H_derived = H.derived_subgroup()
            H_derived_elements = set(H_derived.elements)
            
            K = set()
            for g in G.elements:
                img = phi_func(g)
                if img in H_derived_elements:
                    K.add(g)
                    
            is_subgroup = True
            if not K:
                is_subgroup = False
            else:
                for x in K:
                    for y in K:
                        if (x * ~y) not in K:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                        
            is_normal = True
            if is_subgroup:
                for k in K:
                    for g in G.elements:
                        if (g * k * ~g) not in K:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            else:
                is_normal = False
                
            G_derived = G.derived_subgroup()
            contains_derived = True
            for x in G_derived.elements:
                if x not in K:
                    contains_derived = False
                    break
                    
            Q = is_subgroup and is_normal and contains_derived
            neg_Q = not Q
    except Exception:
        neg_Q = False

    return [h1, h2, neg_Q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a group homomorphism",
    "¬Q: The preimage of the derived subgroup of H is not a normal subgroup of G or does not contain the derived subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2
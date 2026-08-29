import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_identity(G):
    for g in G.elements:
        if g.is_Identity:
            return g
    # Fallback if is_Identity is not found
    return list(G.elements)[0]**0

def conditions(witness):
    try:
        G, H1, H2, phi1, phi2 = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(H1, PermutationGroup) and isinstance(H2, PermutationGroup)
    except Exception:
        h1_ok = False

    phi1_dict = None
    try:
        h2_ok = False
        if h1_ok:
            G_els = list(G.elements)
            H1_els = list(H1.elements)
            if callable(phi1):
                phi1_dict = {g: phi1(g) for g in G_els}
            elif isinstance(phi1, dict):
                phi1_dict = phi1
            
            if phi1_dict is not None and set(phi1_dict.keys()) == set(G_els) and all(v in H1_els for v in phi1_dict.values()):
                h2_ok = True
                for x in G_els:
                    for y in G_els:
                        if phi1_dict[x * y] != phi1_dict[x] * phi1_dict[y]:
                            h2_ok = False
                            break
                    if not h2_ok:
                        break
    except Exception:
        h2_ok = False

    phi2_dict = None
    try:
        h3_ok = False
        if h1_ok:
            G_els = list(G.elements)
            H2_els = list(H2.elements)
            if callable(phi2):
                phi2_dict = {g: phi2(g) for g in G_els}
            elif isinstance(phi2, dict):
                phi2_dict = phi2
            
            if phi2_dict is not None and set(phi2_dict.keys()) == set(G_els) and all(v in H2_els for v in phi2_dict.values()):
                h3_ok = True
    except Exception:
        h3_ok = False

    try:
        neg_q = False
        if h1_ok and h2_ok and h3_ok:
            H1_id = get_identity(H1)
            H2_id = get_identity(H2)
            G_id = get_identity(G)
            
            K1 = {g for g in G.elements if phi1_dict[g] == H1_id}
            K2 = {g for g in G.elements if phi2_dict[g] == H2_id}
            K = K1.intersection(K2)
            
            is_subgroup = True
            if G_id not in K:
                is_subgroup = False
            else:
                for x in K:
                    if x**-1 not in K:
                        is_subgroup = False
                        break
                    for y in K:
                        if x * y not in K:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
            
            is_normal = is_subgroup
            if is_normal:
                for g in G.elements:
                    for x in K:
                        if g * x * (g**-1) not in K:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G, H1, and H2 are groups",
    "H_2: phi1 is a group homomorphism from G to H1",
    "H_3: phi2 is a function from G to H2",
    "¬Q: ker(phi1) ∩ ker(phi2) is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3
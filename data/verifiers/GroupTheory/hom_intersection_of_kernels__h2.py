import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H1 is a group",
    "H_3: H2 is a group",
    "H_4: phi2 is a group homomorphism from G to H2",
    "¬Q: The intersection ker(phi1) ∩ ker(phi2) is not a normal subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H1 = witness['H1']
            H2 = witness['H2']
            phi1 = witness['phi1']
            phi2 = witness['phi2']
        else:
            G, H1, H2, phi1, phi2 = witness
    except Exception:
        return [False] * 5

    # H1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H2: H1 is a group
    try:
        h2_ok = isinstance(H1, PermutationGroup)
    except Exception:
        h2_ok = False

    # H3: H2 is a group
    try:
        h3_ok = isinstance(H2, PermutationGroup)
    except Exception:
        h3_ok = False

    # H4: phi2 is a group homomorphism from G to H2
    try:
        g_elements = list(G.generate())
        h2_elements = list(H2.generate())
        
        if callable(phi2):
            phi2_map = {g: phi2(g) for g in g_elements}
        elif isinstance(phi2, dict):
            phi2_map = phi2
        else:
            raise ValueError
            
        h4_ok = True
        for g in g_elements:
            if g not in phi2_map or phi2_map[g] not in h2_elements:
                h4_ok = False
                break
        if h4_ok:
            for x in g_elements:
                for y in g_elements:
                    if phi2_map[x * y] != phi2_map[x] * phi2_map[y]:
                        h4_ok = False
                        break
                if not h4_ok:
                    break
    except Exception:
        h4_ok = False

    # neg_Q: The intersection ker(phi1) \cap ker(phi2) is NOT a normal subgroup of G
    try:
        g_elements = list(G.generate())
        
        if callable(phi1):
            phi1_map = {g: phi1(g) for g in g_elements}
        elif isinstance(phi1, dict):
            phi1_map = phi1
        else:
            raise ValueError
            
        if callable(phi2):
            phi2_map = {g: phi2(g) for g in g_elements}
        elif isinstance(phi2, dict):
            phi2_map = phi2
        else:
            raise ValueError
            
        ker1 = {g for g in g_elements if phi1_map.get(g) == H1.identity}
        ker2 = {g for g in g_elements if phi2_map.get(g) == H2.identity}
        
        intersection = ker1.intersection(ker2)
        
        is_subgroup = True
        if G.identity not in intersection:
            is_subgroup = False
        else:
            for x in intersection:
                if x**-1 not in intersection:
                    is_subgroup = False
                    break
                for y in intersection:
                    if x * y not in intersection:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
                    
        is_normal = True
        if is_subgroup:
            for n in intersection:
                for g in g_elements:
                    if g * n * g**-1 not in intersection:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
        is_normal_subgroup = is_subgroup and is_normal
        neg_q_ok = not is_normal_subgroup
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]
import sympy as sp
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

def get_identity(G):
    for g in G.elements:
        if g.is_Identity:
            return g
    return list(G.elements)[0] ** 0

def get_presentation_abelian_invariants(X1, X2, R1, R2, A, phi1_X, phi2_X):
    gens = list(set(X1) | set(X2))
    if not gens:
        return []
    F, F_gens = free_group(",".join(gens))
    gen_map = {g: F_gens[i] for i, g in enumerate(gens)}
    
    rels = []
    for r in R1 + R2:
        word = F.identity
        for g, p in r:
            word = word * (gen_map[g] ** p)
        rels.append(word)
        
    for a in list(A.elements):
        word1 = F.identity
        for g, p in phi1_X[a]:
            word1 = word1 * (gen_map[g] ** p)
        word2 = F.identity
        for g, p in phi2_X[a]:
            word2 = word2 * (gen_map[g] ** p)
        rels.append(word1 * (word2 ** -1))
        
    G = FpGroup(F, rels)
    return G.abelian_invariants()

def get_G1_amalgam_G2_abelian_invariants(G1, G2, A):
    inv1 = G1.abelian_invariants()
    inv2 = G2.abelian_invariants()
    
    inv1 = [x for x in inv1 if x != 1]
    inv2 = [x for x in inv2 if x != 1]
    
    gens = [f"a{i}" for i in range(len(inv1))] + [f"b{i}" for i in range(len(inv2))]
    if not gens:
        return []
        
    F, F_gens = free_group(",".join(gens))
    rels = []
    for i, n in enumerate(inv1):
        if n > 0:
            rels.append(F_gens[i]**n)
    for i, n in enumerate(inv2):
        if n > 0:
            rels.append(F_gens[len(inv1) + i]**n)
            
    for i in range(len(gens)):
        for j in range(i + 1, len(gens)):
            rels.append(F_gens[i] * F_gens[j] * F_gens[i]**-1 * F_gens[j]**-1)
            
    G = FpGroup(F, rels)
    return G.abelian_invariants()

def conditions(witness):
    # H1: X1 and X2 are disjoint sets
    try:
        X1 = set(witness['X1'])
        X2 = set(witness['X2'])
        h1 = X1.isdisjoint(X2)
    except Exception:
        h1 = False

    # H2: A is a group
    try:
        A = witness['A']
        h2 = isinstance(A, PermutationGroup)
    except Exception:
        h2 = False

    # H3: phi1 and phi2 are injective group homomorphisms
    try:
        A = witness['A']
        G1 = witness['G1']
        G2 = witness['G2']
        phi1 = witness['phi1']
        phi2 = witness['phi2']
        
        A_elements = list(A.elements)
        h3 = True
        for a in A_elements:
            if a not in phi1 or a not in phi2:
                h3 = False
                break
            if phi1[a] not in G1 or phi2[a] not in G2:
                h3 = False
                break
                
        if h3:
            for a in A_elements:
                for b in A_elements:
                    if phi1[a * b] != phi1[a] * phi1[b]:
                        h3 = False
                        break
                    if phi2[a * b] != phi2[a] * phi2[b]:
                        h3 = False
                        break
                if not h3:
                    break
                    
        if h3:
            id_G1 = get_identity(G1)
            id_G2 = get_identity(G2)
            id_A = get_identity(A)
            for a in A_elements:
                if a != id_A:
                    if phi1[a] == id_G1 or phi2[a] == id_G2:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # neg_Q: The presentation is not isomorphic to the amalgamated free product
    try:
        A = witness['A']
        G1 = witness['G1']
        G2 = witness['G2']
        X1 = witness['X1']
        X2 = witness['X2']
        R1 = witness['R1']
        R2 = witness['R2']
        phi1_X = witness['phi1_X']
        phi2_X = witness['phi2_X']
        
        if A.order() != 1:
            # We only verify non-isomorphism easily when A is trivial
            neg_q = False
        else:
            inv_pres = get_presentation_abelian_invariants(X1, X2, R1, R2, A, phi1_X, phi2_X)
            inv_amalgam = get_G1_amalgam_G2_abelian_invariants(G1, G2, A)
            
            inv_pres = [x for x in inv_pres if x != 1]
            inv_amalgam = [x for x in inv_amalgam if x != 1]
            
            # If the abelian invariants differ, the groups are definitively not isomorphic
            neg_q = sorted(inv_pres) != sorted(inv_amalgam)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X1 and X2 are disjoint sets",
    "H_2: A is a group",
    "H_3: phi1 and phi2 are injective group homomorphisms",
    "¬Q: The presentation is not isomorphic to the amalgamated free product"
]

N_HYP = 3
NEG_Q_INDEX = 3
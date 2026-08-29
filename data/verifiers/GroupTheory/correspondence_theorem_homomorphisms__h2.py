import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_all_subgroups(G):
    elements = list(G.elements)
    subgroups = set()
    
    triv = frozenset([G.identity])
    subgroups.add(triv)
    
    queue = [triv]
    while queue:
        current = queue.pop(0)
        for g in elements:
            if g not in current:
                H_sub = PermutationGroup(list(current) + [g])
                new_subgroup = frozenset(H_sub.elements)
                if new_subgroup not in subgroups:
                    subgroups.add(new_subgroup)
                    queue.append(new_subgroup)
                    
    return subgroups

def posets_are_isomorphic(poset1, poset2):
    if len(poset1) != len(poset2):
        return False
    n = len(poset1)
    if n == 0:
        return True
        
    def build_matrix(poset):
        mat = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if poset[i].issubset(poset[j]):
                    mat[i][j] = True
        return mat
        
    mat1 = build_matrix(poset1)
    mat2 = build_matrix(poset2)
    
    deg1 = [(sum(mat1[i]), sum(mat1[j][i] for j in range(n))) for i in range(n)]
    deg2 = [(sum(mat2[i]), sum(mat2[j][i] for j in range(n))) for i in range(n)]
    
    groups1 = {}
    for i, d in enumerate(deg1):
        if d not in groups1:
            groups1[d] = []
        groups1[d].append(i)
        
    groups2 = {}
    for i, d in enumerate(deg2):
        if d not in groups2:
            groups2[d] = []
        groups2[d].append(i)
        
    if set(groups1.keys()) != set(groups2.keys()):
        return False
        
    for k in groups1:
        if len(groups1[k]) != len(groups2[k]):
            return False
            
    keys = list(groups1.keys())
    
    def search(key_idx, mapping):
        if key_idx == len(keys):
            return True
        k = keys[key_idx]
        cands1 = groups1[k]
        cands2 = groups2[k]
        
        for p in itertools.permutations(cands2):
            valid = True
            new_mapping = mapping.copy()
            for i, c1 in enumerate(cands1):
                new_mapping[c1] = p[i]
                
            mapped_c1 = list(new_mapping.keys())
            for c1_a in mapped_c1:
                for c1_b in mapped_c1:
                    if mat1[c1_a][c1_b] != mat2[new_mapping[c1_a]][new_mapping[c1_b]]:
                        valid = False
                        break
                if not valid:
                    break
                    
            if valid:
                if search(key_idx + 1, new_mapping):
                    return True
        return False

    return search(0, {})

def conditions(witness) -> list[bool]:
    try:
        G, H, f = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = hasattr(G, 'elements') and hasattr(H, 'elements') and hasattr(G, 'identity') and hasattr(H, 'identity')
    except Exception:
        h1 = False
        
    try:
        subgroups_G = get_all_subgroups(G)
        subgroups_H = get_all_subgroups(H)
        
        if isinstance(f, dict):
            ker = frozenset(g for g in G.elements if f[g] == H.identity)
        else:
            ker = frozenset(g for g in G.elements if f(g) == H.identity)
            
        subgroups_G_ker = [sg for sg in subgroups_G if ker.issubset(sg)]
        
        poset1 = list(subgroups_G_ker)
        poset2 = list(subgroups_H)
        
        q = posets_are_isomorphic(poset1, poset2)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "¬Q: There is no inclusion-preserving bijection between subgroups of G containing ker(f) and subgroups of H"
]

N_HYP = 1
NEG_Q_INDEX = 1
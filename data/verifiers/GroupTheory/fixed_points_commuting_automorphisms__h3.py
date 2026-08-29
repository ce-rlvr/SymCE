import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def is_automorphism(G, f):
    try:
        elements = list(G.elements)
        if isinstance(f, dict):
            mapping = f
        else:
            mapping = {x: f(x) for x in elements}
            
        if len(mapping) != len(elements):
            return False
            
        for x in elements:
            if x not in mapping:
                return False
            if mapping[x] not in elements:
                return False
                
        if len(set(mapping.values())) != len(elements):
            return False
            
        for x in elements:
            for y in elements:
                if mapping[x * y] != mapping[x] * mapping[y]:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, alpha, beta = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    h2 = is_automorphism(G, alpha)
    h3 = is_automorphism(G, beta)
    
    try:
        elements = list(G.elements)
        if isinstance(alpha, dict):
            a_map = alpha
        else:
            a_map = {x: alpha(x) for x in elements}
            
        if isinstance(beta, dict):
            b_map = beta
        else:
            b_map = {x: beta(x) for x in elements}
            
        neg_q = False
        for y in elements:
            if a_map[y] == y:
                by = b_map[y]
                if a_map[by] != by:
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: alpha is an automorphism of G",
    "H_3: beta is an automorphism of G",
    "¬Q: There exists y in F_alpha such that beta(y) is not in F_alpha"
]

N_HYP = 3
NEG_Q_INDEX = 3
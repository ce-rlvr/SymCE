import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(group):
    if hasattr(group, 'generate'):
        return list(group.generate())
    elif hasattr(group, 'elements'):
        return list(group.elements)
    else:
        return list(group)

def get_set(obj):
    if hasattr(obj, 'generate'):
        return set(obj.generate())
    elif hasattr(obj, 'elements'):
        return set(obj.elements)
    else:
        return set(obj)

def are_conjugate(G, H, K):
    try:
        G_elems = get_elements(G)
    except Exception:
        return False
        
    if not G_elems:
        return False
        
    # Try element conjugacy first
    is_element = False
    try:
        g = G_elems[0]
        _ = g * H * g**-1
        is_element = True
    except Exception:
        pass
        
    if is_element:
        for g in G_elems:
            try:
                if g * H * g**-1 == K:
                    return True
            except Exception:
                pass
        return False
        
    # Otherwise, treat as sets
    try:
        H_set = get_set(H)
        K_set = get_set(K)
    except Exception:
        return False
        
    for g in G_elems:
        try:
            conj_H = {g * h * g**-1 for h in H_set}
            if conj_H == K_set:
                return True
        except Exception:
            pass
            
    return False

def is_equivalence_relation(G, S):
    try:
        S_list = list(S)
    except Exception:
        return False
        
    n = len(S_list)
    if n == 0:
        return True
        
    R = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            R[i][j] = are_conjugate(G, S_list[i], S_list[j])
            
    # Check reflexivity
    for i in range(n):
        if not R[i][i]:
            return False
            
    # Check symmetry
    for i in range(n):
        for j in range(n):
            if R[i][j] and not R[j][i]:
                return False
                
    # Check transitivity
    for i in range(n):
        for j in range(n):
            if R[i][j]:
                for k in range(n):
                    if R[j][k] and not R[i][k]:
                        return False
                        
    return True

def is_group(G):
    from sympy.combinatorics import PermutationGroup
    if isinstance(G, PermutationGroup):
        return True
    try:
        if hasattr(G, 'is_group') and G.is_group:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        G, S = witness
    except Exception:
        return [False, False]
        
    # H_1: G is a group
    try:
        h1 = is_group(G)
    except Exception:
        h1 = False
        
    # neg_Q: The relation is NOT an equivalence relation on S
    try:
        q = is_equivalence_relation(G, S)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The relation H ~ K <=> exists g in G, gHg^{-1} = K is not an equivalence relation on S"
]

N_HYP = 1
NEG_Q_INDEX = 1
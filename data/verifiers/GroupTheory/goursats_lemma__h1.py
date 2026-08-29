import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_group(G, is_pair=False):
    if isinstance(G, PermutationGroup):
        return True
    if not G:
        return False
    try:
        elements = list(G)
    except Exception:
        return False
        
    if is_pair:
        identity = None
        for e in elements:
            is_id = True
            for a in elements:
                if (e[0]*a[0], e[1]*a[1]) != a or (a[0]*e[0], a[1]*e[1]) != a:
                    is_id = False
                    break
            if is_id:
                identity = e
                break
        if identity is None:
            return False
            
        for a in elements:
            has_inv = False
            for b in elements:
                prod = (a[0]*b[0], a[1]*b[1])
                if prod not in elements:
                    return False
                if prod == identity and (b[0]*a[0], b[1]*a[1]) == identity:
                    has_inv = True
            if not has_inv:
                return False
        return True
    else:
        identity = None
        for e in elements:
            is_id = True
            for a in elements:
                if e*a != a or a*e != a:
                    is_id = False
                    break
            if is_id:
                identity = e
                break
        if identity is None:
            return False
            
        for a in elements:
            has_inv = False
            for b in elements:
                prod = a*b
                if prod not in elements:
                    return False
                if prod == identity and b*a == identity:
                    has_inv = True
            if not has_inv:
                return False
        return True

def is_normal(N, G):
    if not N or not G:
        return False
    identity = None
    for e in G:
        is_id = True
        for a in G:
            if e*a != a or a*e != a:
                is_id = False
                break
        if is_id:
            identity = e
            break
    if identity is None:
        return False
        
    for g in G:
        g_inv = None
        for b in G:
            if g*b == identity and b*g == identity:
                g_inv = b
                break
        if g_inv is None:
            return False
        for n in N:
            if g * n * g_inv not in N:
                return False
    return True

def check_conclusion(G, H, S):
    if not is_group(G):
        return False
    if not is_group(H):
        return False
        
    A_prime = []
    for g, h in S:
        if g not in A_prime:
            A_prime.append(g)
            
    B_prime = []
    for g, h in S:
        if h not in B_prime:
            B_prime.append(h)
            
    id_S = None
    for e in S:
        is_id = True
        for a in S:
            if (e[0]*a[0], e[1]*a[1]) != a or (a[0]*e[0], a[1]*e[1]) != a:
                is_id = False
                break
        if is_id:
            id_S = e
            break
    if id_S is None:
        return False
    e_g, e_h = id_S
    
    A = []
    for g, h in S:
        if h == e_h and g not in A:
            A.append(g)
            
    B = []
    for g, h in S:
        if g == e_g and h not in B:
            B.append(h)
            
    if not all(x in G for x in A_prime): return False
    if not all(x in H for x in B_prime): return False
    
    if not all(x in A_prime for x in A): return False
    if not all(x in B_prime for x in B): return False
    
    if not is_normal(A, A_prime): return False
    if not is_normal(B, B_prime): return False
    
    return True

def conditions(witness):
    try:
        G, H, S = witness
        S = list(S)
        if not isinstance(H, PermutationGroup):
            H = list(H)
        if not isinstance(G, PermutationGroup):
            G = list(G)
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = is_group(H)
    except Exception:
        h1_ok = False
        
    try:
        s_is_group = is_group(S, is_pair=True)
        s_subset = True
        for g, h in S:
            if g not in G or h not in H:
                s_subset = False
                break
        h2_ok = s_is_group and s_subset
    except Exception:
        h2_ok = False
        
    try:
        conclusion = check_conclusion(G, H, S)
        neg_Q = not conclusion
    except Exception:
        neg_Q = True
        
    return [h1_ok, h2_ok, neg_Q]

CONDITION_LABELS = [
    "H_1: H is a group",
    "H_2: S is a subgroup of G × H",
    "¬Q: There do not exist subgroups A ◁ A' ≤ G and B ◁ B' ≤ H satisfying the Goursat isomorphism condition"
]

N_HYP = 2
NEG_Q_INDEX = 2
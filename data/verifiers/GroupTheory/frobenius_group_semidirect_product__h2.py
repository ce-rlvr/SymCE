import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
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
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def unpack_witness(witness):
    if isinstance(witness, dict):
        return witness.get('G'), witness.get('H'), witness.get('K')
    elif isinstance(witness, (list, tuple)) and len(witness) == 3:
        return witness[0], witness[1], witness[2]
    return None, None, None

def get_identity(G):
    for e in G.elements:
        if e * e == e:
            return e
    return None

def is_subgroup_elements(G, sub_elements):
    if not sub_elements: return False
    G_id = get_identity(G)
    if G_id not in sub_elements: return False
    G_elements = set(G.elements)
    for a in sub_elements:
        if a not in G_elements: return False
        for b in sub_elements:
            if a * b not in sub_elements:
                return False
    return True

def is_frobenius_complement(G, H_elements):
    n_H = len(H_elements)
    n_G = G.order()
    if n_H == 1 or n_H == n_G:
        return False
    G_id = get_identity(G)
    H_non_id = H_elements - {G_id}
    for g in G.elements:
        if g in H_elements:
            continue
        g_inv = g**-1
        for h in H_non_id:
            if g * h * g_inv in H_elements:
                return False
    return True

def check_H1(witness):
    G, H, K = unpack_witness(witness)
    if G is None or H is None or K is None: return False
    if not getattr(G, 'is_group', False): return False
    try:
        if G.order() >= 1000: return False
    except Exception:
        return False
    
    try:
        H_elements = set(H.elements)
        if is_subgroup_elements(G, H_elements) and is_frobenius_complement(G, H_elements):
            return True
    except Exception:
        pass
        
    try:
        G_id = get_identity(G)
        for g in G.elements:
            if g == G_id: continue
            sub = set()
            curr = g
            while curr not in sub:
                sub.add(curr)
                curr = curr * g
            if is_frobenius_complement(G, sub):
                return True
    except Exception:
        pass
        
    return False

def check_H2(witness):
    G, H, K = unpack_witness(witness)
    if G is None or H is None or K is None: return False
    if not getattr(G, 'is_group', False): return False
    if not getattr(H, 'is_group', False): return False
    try:
        H_elements = set(H.elements)
        if not is_subgroup_elements(G, H_elements): return False
        return is_frobenius_complement(G, H_elements)
    except Exception:
        return False

def check_neg_Q(witness):
    G, H, K = unpack_witness(witness)
    if G is None or H is None or K is None: return False
    if not getattr(G, 'is_group', False): return False
    if not getattr(H, 'is_group', False): return False
    if not getattr(K, 'is_group', False): return False
    
    try:
        K_elements = set(K.elements)
        H_elements = set(H.elements)
        
        if not is_subgroup_elements(G, K_elements): return True
        if not is_subgroup_elements(G, H_elements): return True
        
        for g in G.elements:
            g_inv = g**-1
            for k in K_elements:
                if g * k * g_inv not in K_elements:
                    return True
                    
        if len(K_elements.intersection(H_elements)) != 1:
            return True
            
        if len(K_elements) * len(H_elements) != G.order():
            return True
            
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        h1 = check_H1(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2(witness)
    except Exception:
        h2 = False
        
    try:
        neg_q = check_neg_Q(witness)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite Frobenius group",
    "H_2: H is a Frobenius complement of G",
    "¬Q: G is not isomorphic to the internal semidirect product K ⋊ H"
]

N_HYP = 2
NEG_Q_INDEX = 2
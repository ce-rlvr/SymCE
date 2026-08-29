import sympy
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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def check_normal(G, N):
    try:
        if hasattr(G, 'is_normal'):
            res = G.is_normal(N) if callable(G.is_normal) else G.is_normal
            if res is not None: return bool(res)
    except Exception: pass
    try:
        if hasattr(N, 'is_normal'):
            res = N.is_normal(G) if callable(N.is_normal) else N.is_normal
            if res is not None: return bool(res)
    except Exception: pass
    try:
        if hasattr(G, 'is_normal_subgroup'):
            res = G.is_normal_subgroup(N) if callable(G.is_normal_subgroup) else G.is_normal_subgroup
            if res is not None: return bool(res)
    except Exception: pass
    try:
        if hasattr(G, 'elements') and hasattr(N, 'elements'):
            N_elems = set(N.elements)
            for g in G.elements:
                for n in N_elems:
                    if g * n * (g**-1) not in N_elems:
                        return False
            return True
    except Exception: pass
    try:
        if hasattr(G, 'normal'):
            res = G.normal(N) if callable(G.normal) else G.normal
            if res is not None: return bool(res)
    except Exception: pass
    return False

def get_k(G):
    if hasattr(G, 'k_G'):
        val = G.k_G() if callable(G.k_G) else G.k_G
        if val is not None: return val
    if hasattr(G, 'k'):
        val = G.k() if callable(G.k) else G.k
        if val is not None: return val
    if hasattr(G, 'conjugacy_classes'):
        classes = G.conjugacy_classes
        if callable(classes):
            classes = classes()
        return len(classes)
    raise ValueError("Cannot find k(G)")

def get_k_quotient(G, N):
    if hasattr(G, 'k_GN'):
        val = G.k_GN(N) if callable(G.k_GN) else G.k_GN
        if val is not None: return val
    if hasattr(G, 'quotient_k'):
        val = G.quotient_k(N) if callable(G.quotient_k) else G.quotient_k
        if val is not None: return val
    if hasattr(G, 'quotient'):
        Q = G.quotient(N) if callable(G.quotient) else G.quotient
        return get_k(Q)
    if hasattr(G, 'elements') and hasattr(N, 'elements'):
        elements = list(G.elements)
        n_elements = list(N.elements)
        cosets = []
        for g in elements:
            c = frozenset([g * n for n in n_elements])
            if c not in cosets:
                cosets.append(c)
        classes = []
        for c in cosets:
            cls = frozenset([frozenset([g * x * (g**-1) for x in c]) for g in elements])
            if cls not in classes:
                classes.append(cls)
        return len(classes)
    raise ValueError("Cannot find k(G/N)")

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                G, N, k_G, k_GN = witness
            elif len(witness) == 2:
                G, N = witness
                k_G = get_k(G)
                k_GN = get_k_quotient(G, N)
            else:
                return [False, False, False, False]
        elif isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            k_G = witness.get('k_G')
            k_GN = witness.get('k_GN')
        else:
            G = getattr(witness, 'G', witness)
            N = getattr(witness, 'N', witness)
            k_G = getattr(witness, 'k_G', None)
            k_GN = getattr(witness, 'k_GN', None)
            if k_G is None:
                k_G = get_k(G)
            if k_GN is None:
                k_GN = get_k_quotient(G, N)
                
        h1 = check_normal(G, N)
        
        try:
            actual_k_G = get_k(G)
            h2 = (k_G == actual_k_G) and (k_G is not None)
        except Exception:
            h2 = False
            
        try:
            actual_k_GN = get_k_quotient(G, N)
            h3 = (k_GN == actual_k_GN) and (k_GN is not None)
        except Exception:
            h3 = False
            
        if k_GN is not None and k_G is not None:
            neg_q = (k_GN > k_G)
            
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: k(G) is the number of conjugacy classes of G",
    "H_3: k(G/N) is the number of conjugacy classes of the quotient group G/N",
    "¬Q: k(G/N) > k(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory import isprime
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: H is a p-subgroup of G",
    "¬Q: H \\cap N_G(P) \\neq H \\cap P"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_order(G):
    try:
        return G.order()
    except TypeError:
        return G.order

def is_finite_group(G):
    try:
        if isinstance(G, PermutationGroup):
            return True
        o = get_order(G)
        return o > 0 and o != float('inf')
    except Exception:
        return False

def is_subgroup(sub, G):
    try:
        return sub.is_subgroup(G)
    except Exception:
        for g in sub.generators:
            if g not in G:
                return False
        return True

def is_sylow_p_subgroup(P, G, p):
    if not isprime(p): 
        return False
    if not is_subgroup(P, G): 
        return False
    
    order_P = get_order(P)
    order_G = get_order(G)
    
    if order_P != 1:
        temp = order_P
        while temp % p == 0:
            temp //= p
        if temp != 1:
            return False
            
    if order_G % (order_P * p) == 0:
        return False
        
    return True

def is_p_subgroup(H, G, p):
    if not isprime(p): 
        return False
    if not is_subgroup(H, G): 
        return False
        
    order_H = get_order(H)
    if order_H == 1:
        return True
        
    temp = order_H
    while temp % p == 0:
        temp //= p
    return temp == 1

def neg_q(G, P, H, p):
    try:
        elements = H.elements
    except Exception:
        elements = list(H.generate())
        
    for x in elements:
        if x not in P:
            normalizes = True
            for g in P.generators:
                conj = x * g * (x**-1)
                if conj not in P:
                    normalizes = False
                    break
            if normalizes:
                return True
    return False

def conditions(witness):
    try:
        G, P, H, p = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = is_finite_group(G)
    except Exception:
        h1 = False
        
    try:
        h2 = is_sylow_p_subgroup(P, G, p)
    except Exception:
        h2 = False
        
    try:
        h3 = is_p_subgroup(H, G, p)
    except Exception:
        h3 = False
        
    try:
        nq = neg_q(G, P, H, p)
    except Exception:
        nq = False
        
    return [bool(h1), bool(h2), bool(h3), bool(nq)]
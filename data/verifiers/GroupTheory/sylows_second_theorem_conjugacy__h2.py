import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Top-level setup: named object bindings
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

def pad_perm(p, degree):
    arr = p.array_form
    if len(arr) < degree:
        arr = arr + list(range(len(arr), degree))
        return Permutation(arr)
    elif len(arr) > degree:
        return Permutation(arr[:degree])
    return p

def perm_in_group(p, G):
    degree = G.degree
    arr = p.array_form
    if len(arr) < degree:
        arr = arr + list(range(len(arr), degree))
        p_adj = Permutation(arr)
    elif len(arr) > degree:
        for i in range(degree, len(arr)):
            if arr[i] != i:
                return False
        p_adj = Permutation(arr[:degree])
    else:
        p_adj = p
    return p_adj in G

def is_subgroup_safe(G, H):
    if not isinstance(H, PermutationGroup):
        return False
    for g in H.generators:
        if not perm_in_group(g, G):
            return False
    return True

def is_sylow(G, H):
    if not is_subgroup_safe(G, H):
        return False
    order_H = H.order()
    order_G = G.order()
    if order_H == 1:
        return True
    factors = factorint(order_H)
    if len(factors) != 1:
        return False
    p = list(factors.keys())[0]
    max_pow = 1
    temp = order_G
    while temp % p == 0:
        max_pow *= p
        temp //= p
    return order_H == max_pow

def are_conjugate(G, P, Q):
    if P.order() != Q.order():
        return False
    degree = G.degree
    for g in G.elements:
        is_conj = True
        for p in P.generators:
            p_adj = pad_perm(p, degree)
            conj_p = g * p_adj * (~g)
            if not perm_in_group(conj_p, Q):
                is_conj = False
                break
        if is_conj:
            return True
    return False

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False, False]
        G, P, Q = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: P is a Sylow p-subgroup of G
    try:
        h2 = is_sylow(G, P)
    except Exception:
        h2 = False
        
    # H_3: Q is a Sylow p-subgroup of G
    try:
        h3 = is_sylow(G, Q)
    except Exception:
        h3 = False
        
    # ¬Q: There does NOT exist an element g in G such that gPg^{-1} = Q
    try:
        neg_q = not are_conjugate(G, P, Q)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: Q is a Sylow p-subgroup of G",
    "¬Q: P and Q are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3
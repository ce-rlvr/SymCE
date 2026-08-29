import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Setup named objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_in_group(p, G):
    arr = list(p.array_form)
    degree = G.degree
    while len(arr) > degree and arr[-1] == len(arr) - 1:
        arr.pop()
    if len(arr) > degree:
        return False
    try:
        p_new = Permutation(arr, size=degree)
        return G.contains(p_new)
    except Exception:
        return False

def get_normalized_elements(H, degree):
    elements = set()
    if hasattr(H, 'generate'):
        gen = H.generate()
    else:
        gen = H
    for p in gen:
        if not isinstance(p, Permutation):
            continue
        arr = list(p.array_form)
        while len(arr) > degree and arr[-1] == len(arr) - 1:
            arr.pop()
        if len(arr) > degree:
            continue
        try:
            p_new = Permutation(arr, size=degree)
            elements.add(p_new)
        except Exception:
            pass
    return elements

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() < float('inf')
    except Exception:
        h1 = False
        
    # H2: K is a subgroup of G
    try:
        if isinstance(K, PermutationGroup) and isinstance(G, PermutationGroup):
            h2 = all(is_in_group(g, G) for g in K.generators)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: gcd([G:H], [G:K]) == 1
    try:
        if not isinstance(G, PermutationGroup):
            h3 = False
        else:
            order_G = G.order()
            
            if hasattr(H, 'order'):
                order_H = H.order()
            else:
                order_H = len(get_normalized_elements(H, G.degree))
                
            if hasattr(K, 'order'):
                order_K = K.order()
            else:
                order_K = len(get_normalized_elements(K, G.degree))
                
            if order_H > 0 and order_K > 0 and order_G % order_H == 0 and order_G % order_K == 0:
                idx_H = order_G // order_H
                idx_K = order_G // order_K
                h3 = math.gcd(idx_H, idx_K) == 1
            else:
                h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: [G: H \cap K] != [G:H] * [G:K]
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            degree = G.degree
            elements_H = get_normalized_elements(H, degree)
            elements_K = get_normalized_elements(K, degree)
            
            intersection = elements_H.intersection(elements_K)
            order_int = len(intersection)
            
            order_G = G.order()
            if hasattr(H, 'order'):
                order_H = H.order()
            else:
                order_H = len(elements_H)
                
            if hasattr(K, 'order'):
                order_K = K.order()
            else:
                order_K = len(elements_K)
                
            if order_H == 0 or order_K == 0:
                neg_q = False
            else:
                idx_H = order_G / order_H
                idx_K = order_G / order_K
                
                if order_int == 0:
                    neg_q = True
                else:
                    idx_int = order_G / order_int
                    neg_q = abs(idx_int - idx_H * idx_K) > 1e-9
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: K is a subgroup of G",
    "H_3: The greatest common divisor of the index of H and the index of K is 1",
    "¬Q: The index of H intersect K is not equal to the product of their indices"
]

N_HYP = 3
NEG_Q_INDEX = 3
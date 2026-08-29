import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_elements(S):
    if hasattr(S, 'generate') and callable(S.generate):
        return set(S.generate())
    elif hasattr(S, 'elements'):
        return set(S.elements)
    else:
        return set(S)

def get_order(S):
    if hasattr(S, 'order') and callable(S.order):
        return S.order()
    else:
        return len(get_elements(S))

def get_index(G, S):
    order_G = get_order(G)
    if order_G == sympy.oo:
        return float('inf')
    order_S = get_order(S)
    if order_S == 0 or order_G % order_S != 0:
        return float('inf')
    return order_G // order_S

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False] * 6

    try:
        h1 = isinstance(G, PermutationGroup) or getattr(G, 'is_group', False)
    except Exception:
        h1 = False

    try:
        h2 = False
        if isinstance(K, PermutationGroup) or getattr(K, 'is_group', False):
            if hasattr(K, 'is_subgroup'):
                try:
                    h2 = K.is_subgroup(G)
                except Exception:
                    pass
            if not h2:
                elems_K = get_elements(K)
                elems_G = get_elements(G)
                h2 = elems_K.issubset(elems_G)
        else:
            elems_K = get_elements(K)
            elems_G = get_elements(G)
            if elems_K and elems_K.issubset(elems_G):
                closed = True
                for k1 in elems_K:
                    for k2 in elems_K:
                        if (k1 * k2) not in elems_K:
                            closed = False
                            break
                    if not closed:
                        break
                h2 = closed
    except Exception:
        h2 = False

    try:
        idx_H = get_index(G, H)
        h3 = (idx_H < float('inf'))
    except Exception:
        h3 = False

    try:
        idx_K = get_index(G, K)
        h4 = (idx_K < float('inf'))
    except Exception:
        h4 = False

    try:
        if h3 and h4:
            h5 = (math.gcd(int(idx_H), int(idx_K)) == 1)
        else:
            h5 = False
    except Exception:
        h5 = False

    try:
        elems_H = get_elements(H)
        elems_K = get_elements(K)
        elems_G = get_elements(G)
        
        HK = set()
        for h in elems_H:
            for k in elems_K:
                HK.add(h * k)
                
        neg_Q = (elems_G != HK)
    except Exception:
        neg_Q = False

    return [h1, h2, h3, h4, h5, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a subgroup of G",
    "H_3: The index of H in G is finite",
    "H_4: The index of K in G is finite",
    "H_5: The greatest common divisor of the indices is 1",
    "¬Q: G != HK"
]

N_HYP = 5
NEG_Q_INDEX = 5
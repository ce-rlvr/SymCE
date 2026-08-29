import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.matrices import eye, zeros
import math

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

def get_index(G, H):
    if hasattr(G, 'index') and callable(G.index):
        try:
            return G.index(H)
        except Exception:
            pass
    g_ord = G.order()
    h_ord = H.order()
    if g_ord == sympy.oo or h_ord == sympy.oo:
        raise ValueError("Infinite order")
    ans = g_ord / h_ord
    if ans == int(ans):
        return int(ans)
    raise ValueError("Not an integer index")

def get_elements(grp):
    if hasattr(grp, 'generate') and callable(grp.generate):
        return list(grp.generate())
    if hasattr(grp, 'elements'):
        return list(grp.elements)
    return list(grp)

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False] * 5 + [False]
        
    try:
        h1 = bool(H.is_subgroup(G))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(K.is_subgroup(G))
    except Exception:
        h2 = False
        
    try:
        idx_H = get_index(G, H)
        h3 = True
    except Exception:
        h3 = False
        
    try:
        idx_K = get_index(G, K)
        h4 = True
    except Exception:
        h4 = False
        
    try:
        idx_H = get_index(G, H)
        idx_K = get_index(G, K)
        h5 = (math.gcd(idx_H, idx_K) == 1)
    except Exception:
        h5 = False
        
    try:
        if hasattr(G, 'order') and G.order() != sympy.oo:
            try:
                if hasattr(H, 'intersect'):
                    int_HK = H.intersect(K)
                elif hasattr(H, 'intersection'):
                    int_HK = H.intersection(K)
                else:
                    raise AttributeError
                size_HK = (H.order() * K.order()) // int_HK.order()
                neg_q = (G.order() != size_HK)
            except Exception:
                H_elems = get_elements(H)
                K_elems = get_elements(K)
                hk_set = set()
                for h in H_elems:
                    for k in K_elems:
                        hk_set.add(h * k)
                neg_q = (len(hk_set) != G.order())
        else:
            if hasattr(G, 'equals_HK'):
                neg_q = not G.equals_HK(H, K)
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: K is a subgroup of G",
    "H_3: The index of H in G is finite",
    "H_4: The index of K in G is finite",
    "H_5: The greatest common divisor of the indices is 1",
    "¬Q: G is not equal to HK"
]

N_HYP = 5
NEG_Q_INDEX = 5
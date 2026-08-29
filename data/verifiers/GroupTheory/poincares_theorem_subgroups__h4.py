import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, oo

# --- Top-level setup ---

class Z_subgroup:
    def __init__(self, n):
        self.n = abs(n)
        
    def intersection(self, other):
        if self.n == 0 or other.n == 0:
            return Z_subgroup(0)
        return Z_subgroup(abs(self.n * other.n) // math.gcd(self.n, other.n))
        
    def index_in(self, parent):
        if self.n == parent.n:
            return 1
        if self.n == 0:
            return math.inf
        if parent.n == 0:
            raise ValueError("Not a subgroup")
        return self.n // parent.n
        
    def is_subgroup_of(self, parent):
        if parent.n == 0:
            return self.n == 0
        return self.n % parent.n == 0
        
    @property
    def is_group(self):
        return True
        
    def __repr__(self):
        return f"Z_subgroup({self.n})"

# The infinite cyclic group Z
Z = Z_subgroup(1)

# Standard finite groups for fallback/testing
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


def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False] * 5
    
    # H_1: G is a group
    try:
        if isinstance(G, Z_subgroup):
            h1 = True
        else:
            h1 = getattr(G, 'is_group', False)
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        if isinstance(H, Z_subgroup) and isinstance(G, Z_subgroup):
            h2 = H.is_subgroup_of(G)
        else:
            h2 = H.is_subgroup(G)
    except Exception:
        h2 = False
        
    # H_3: K is a subgroup of G
    try:
        if isinstance(K, Z_subgroup) and isinstance(G, Z_subgroup):
            h3 = K.is_subgroup_of(G)
        else:
            h3 = K.is_subgroup(G)
    except Exception:
        h3 = False
        
    # H_4: The index of K in G is finite
    try:
        if isinstance(K, Z_subgroup) and isinstance(G, Z_subgroup):
            idx_K = K.index_in(G)
        else:
            idx_K = G.order() // K.order()
        h4 = (idx_K != math.inf) and (idx_K != oo)
    except Exception:
        h4 = False
        
    # neg_Q: The intersection of H and K has finite index in G, and index <= index_H * index_K
    # We need the NEGATION of this conclusion.
    try:
        if isinstance(H, Z_subgroup) and isinstance(K, Z_subgroup) and isinstance(G, Z_subgroup):
            H_cap_K = H.intersection(K)
            idx_H_cap_K = H_cap_K.index_in(G)
            idx_H = H.index_in(G)
            idx_K = K.index_in(G)
        else:
            try:
                H_cap_K = H.intersect(K)
            except AttributeError:
                H_cap_K = H.intersection(K)
            idx_H_cap_K = G.order() // H_cap_K.order()
            idx_H = G.order() // H.order()
            idx_K = G.order() // K.order()
            
        Q = (idx_H_cap_K != math.inf) and (idx_H_cap_K != oo) and (idx_H_cap_K <= idx_H * idx_K)
        neg_q = not Q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]


CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of G",
    "H_4: The index of K in G is finite",
    "not Q: The intersection of H and K has infinite index or its index exceeds the product of indices"
]

N_HYP = 4
NEG_Q_INDEX = 4
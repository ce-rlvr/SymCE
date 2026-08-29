import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: N is a normal subgroup of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: P \\cap N is not a Sylow p-subgroup of N"
]

class SimpleGroup:
    """A lightweight group representation for intersections to avoid PermutationGroup overhead."""
    def __init__(self, elements):
        self.elements = list(elements)
        
    def order(self):
        return len(self.elements)
        
    @property
    def generators(self):
        return self.elements
        
    def is_subgroup(self, G):
        try:
            for g in self.elements:
                if g not in G:
                    return False
            return True
        except Exception:
            return False

def is_subgroup(H, G):
    if hasattr(H, 'is_subgroup'):
        try:
            return H.is_subgroup(G)
        except Exception:
            pass
    if hasattr(G, 'has_subgroup'):
        try:
            return G.has_subgroup(H)
        except Exception:
            pass
            
    try:
        for g in H.generators:
            if g not in G:
                return False
        return True
    except Exception:
        return False

def is_normal_subgroup(N, G):
    if hasattr(N, 'is_normal'):
        try:
            return N.is_normal(G)
        except Exception:
            pass
            
    if not is_subgroup(N, G):
        return False
        
    try:
        for g in G.generators:
            for n in N.generators:
                try:
                    inv_g = ~g
                except Exception:
                    inv_g = g**-1
                if (g * n * inv_g) not in N:
                    return False
        return True
    except Exception:
        return False

def is_sylow_p_subgroup(H, G, p):
    if hasattr(H, 'is_sylow_p_subgroup'):
        try:
            return H.is_sylow_p_subgroup(G, p)
        except Exception:
            pass
    if hasattr(G, 'is_sylow_p_subgroup'):
        try:
            return G.is_sylow_p_subgroup(H, p)
        except Exception:
            pass
            
    if not is_subgroup(H, G):
        return False
        
    try:
        order_G = G.order()
        order_H = H.order()
    except Exception:
        return False
        
    if order_G == sympy.oo:
        raise ValueError("Cannot determine Sylow p-subgroup for infinite group without custom methods")
        
    try:
        k = 0
        temp = order_G
        while temp > 0 and temp % p == 0:
            k += 1
            temp //= p
            
        return order_H == p**k
    except Exception:
        return False

def get_intersection(G1, G2):
    if hasattr(G1, 'intersect'):
        try:
            return G1.intersect(G2)
        except Exception:
            pass
    if hasattr(G1, 'intersection'):
        try:
            return G1.intersection(G2)
        except Exception:
            pass
            
    try:
        elems1 = set(G1.generate())
        elems2 = set(G2.generate())
        common = elems1.intersection(elems2)
        return SimpleGroup(common)
    except Exception:
        pass
        
    try:
        return G1.intersection(G2)
    except Exception:
        pass
        
    raise ValueError("Cannot compute intersection")

def conditions(witness):
    try:
        G, N, P, p = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = bool(is_normal_subgroup(N, G))
    except Exception:
        h2_ok = False
        
    try:
        h3_ok = bool(is_sylow_p_subgroup(P, G, p))
    except Exception:
        h3_ok = False
        
    try:
        int_PN = get_intersection(P, N)
        if int_PN is None:
            neg_q = False
        else:
            is_sylow = is_sylow_p_subgroup(int_PN, N, p)
            neg_q = not bool(is_sylow)
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q]
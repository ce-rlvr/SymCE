import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup: named object bindings
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

def get_order(group):
    order = group.order
    if callable(order):
        return order()
    return order

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    # H_3: The greatest common divisor of the order of H and the index of N in G is 1
    try:
        h_order = int(get_order(H))
        g_order = int(get_order(G))
        n_order = int(get_order(N))
        index = g_order // n_order
        # Implicitly H should be a subgroup of G for the theorem context to make sense
        h3 = math.gcd(h_order, index) == 1 and H.is_subgroup(G)
    except Exception:
        h3 = False
        
    # ¬Q: H is not a subgroup of N
    try:
        neg_q = not H.is_subgroup(N)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: The greatest common divisor of the order of H and the index of N in G is 1",
    "¬Q: H is not a subgroup of N"
]

N_HYP = 3
NEG_Q_INDEX = 3
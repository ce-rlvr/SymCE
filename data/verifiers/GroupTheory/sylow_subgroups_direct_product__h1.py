import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def is_sylow_p_subgroup(P, G, p):
    try:
        if not P.is_subgroup(G):
            return False
        order_P = P.order()
        order_G = G.order()
        
        # Check if P is a p-group
        if order_P > 1:
            factors = sympy.factorint(order_P)
            if len(factors) != 1 or p not in factors:
                return False
        elif order_P != 1:
            return False
            
        # Check if the index of P in G is coprime to p
        if (order_G // order_P) % p == 0:
            return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        p, P, G, Q, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    # H_2: P is a Sylow p-subgroup of G
    h2 = is_sylow_p_subgroup(P, G, p)
    
    # H_3: Q is a Sylow p-subgroup of H
    h3 = is_sylow_p_subgroup(Q, H, p)
    
    # ¬Q: P × Q is not a Sylow p-subgroup of G × H
    try:
        PxQ = P * Q
        GxH = G * H
        is_sylow = is_sylow_p_subgroup(PxQ, GxH, p)
        neg_q = not is_sylow
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: Q is a Sylow p-subgroup of H",
    "¬Q: P × Q is not a Sylow p-subgroup of G × H"
]

N_HYP = 3
NEG_Q_INDEX = 3
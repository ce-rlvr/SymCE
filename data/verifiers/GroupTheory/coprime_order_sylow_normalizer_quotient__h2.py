import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, P, p = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() < float('inf')
    except Exception:
        h1 = False
        
    # H2: P is a Sylow p-subgroup of G
    try:
        h2 = False
        if h1 and isinstance(P, PermutationGroup):
            # Check if P is a subgroup of G
            is_sub = True
            for gen in P.generators:
                if not G.contains(gen):
                    is_sub = False
                    break
            
            if is_sub:
                order_P = P.order()
                order_G = G.order()
                
                if isinstance(p, int) and p > 1:
                    # Check if order_P is a power of p
                    temp = order_P
                    while temp % p == 0 and temp > 1:
                        temp //= p
                    
                    if temp == 1:
                        # Check if order_P is the highest power of p dividing order_G
                        if order_G % order_P == 0 and order_G % (order_P * p) != 0:
                            h2 = True
                elif p == 1:
                    if order_P == 1:
                        h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: The order of the quotient group N_G(P) / P is NOT coprime to p
    try:
        neg_q = False
        if h1 and h2:
            P_gens = P.generators
            norm_order = 0
            
            # Compute the order of the normalizer N_G(P)
            for g in G.generate():
                is_in_normalizer = True
                for p_gen in P_gens:
                    # Conjugate p_gen by g
                    conj = g * p_gen * (~g)
                    if not P.contains(conj):
                        is_in_normalizer = False
                        break
                if is_in_normalizer:
                    norm_order += 1
            
            quotient_order = norm_order // P.order()
            
            # The conclusion fails if the quotient order is NOT coprime to p
            if math.gcd(quotient_order, p) != 1:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: The order of the quotient group N_G(P) / P is not coprime to p"
]

N_HYP = 2
NEG_Q_INDEX = 2
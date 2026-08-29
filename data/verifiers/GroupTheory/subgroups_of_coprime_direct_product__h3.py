import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, H, S = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are finite groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
        if h1:
            _ = G.order()
            _ = H.order()
    except Exception:
        h1 = False
        
    # H_2: The greatest common divisor of the order of G and the order of H is 1
    try:
        h2 = math.gcd(int(G.order()), int(H.order())) == 1
    except Exception:
        h2 = False
        
    # ¬Q: S is not of the form A x B for any A <= G, B <= H
    try:
        if not isinstance(S, PermutationGroup):
            neg_q = False
        else:
            order_G = int(G.order())
            order_H = int(H.order())
            order_S = int(S.order())
            
            possible_orders = set()
            for a in range(1, order_G + 1):
                if order_G % a == 0:
                    for b in range(1, order_H + 1):
                        if order_H % b == 0:
                            possible_orders.add(a * b)
                            
            if order_S not in possible_orders:
                neg_q = True
            elif G.is_abelian and H.is_abelian and not S.is_abelian:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: The greatest common divisor of the order of G and the order of H is 1",
    "¬Q: S is not of the form A x B for any A <= G, B <= H"
]

N_HYP = 2
NEG_Q_INDEX = 2
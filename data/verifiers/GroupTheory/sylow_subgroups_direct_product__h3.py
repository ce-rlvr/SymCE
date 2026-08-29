import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

def highest_power(n, p):
    if p <= 1 or n <= 0:
        return 1
    count = 0
    while n % p == 0:
        count += 1
        n //= p
    return p ** count

def conditions(witness):
    try:
        G, H, p, P, Q = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G and H are finite groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: p is a prime number
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False
        
    # H3: Q is a Sylow p-subgroup of H
    try:
        if isinstance(Q, PermutationGroup) and isinstance(H, PermutationGroup) and Q.is_subgroup(H):
            expected_Q = highest_power(H.order(), p)
            h3 = (Q.order() == expected_Q)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: P x Q is NOT a Sylow p-subgroup of G x H
    try:
        if not (isinstance(P, PermutationGroup) and isinstance(Q, PermutationGroup)):
            neg_q_val = True
        elif not (P.is_subgroup(G) and Q.is_subgroup(H)):
            neg_q_val = True
        else:
            order_PxQ = P.order() * Q.order()
            expected_PxQ = highest_power(G.order() * H.order(), p)
            neg_q_val = (order_PxQ != expected_PxQ)
    except Exception:
        neg_q_val = True
        
    return [h1, h2, h3, neg_q_val]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: p is a prime number",
    "H_3: Q is a Sylow p-subgroup of H",
    "¬Q: P x Q is not a Sylow p-subgroup of G x H"
]

N_HYP = 3
NEG_Q_INDEX = 3
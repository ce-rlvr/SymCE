import sympy
from sympy import isprime
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def safe_is_subgroup(H, G):
    try:
        if hasattr(H, 'is_subgroup'):
            res = H.is_subgroup(G)
            if isinstance(res, bool):
                return res
    except Exception:
        pass
    try:
        for gen in H.generators:
            if not G.contains(gen):
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, p, q, P, Q = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: p and q are distinct primes
    try:
        h1 = bool(isprime(p) and isprime(q) and p != q)
    except Exception:
        h1 = False
        
    # H2: P is a Sylow p-subgroup of G
    try:
        if not safe_is_subgroup(P, G):
            h2 = False
        else:
            order_G = G.order()
            order_P = P.order()
            k = 0
            while order_G % (p**(k+1)) == 0:
                k += 1
            h2 = bool(order_P == p**k)
    except Exception:
        h2 = False
        
    # H3: Q is a Sylow q-subgroup of G
    try:
        if not safe_is_subgroup(Q, G):
            h3 = False
        else:
            order_G = G.order()
            order_Q = Q.order()
            m = 0
            while order_G % (q**(m+1)) == 0:
                m += 1
            h3 = bool(order_Q == q**m)
    except Exception:
        h3 = False
        
    # Negated Conclusion: P \cap Q is NOT the trivial subgroup {1}
    try:
        if P.order() < Q.order():
            small, large = P, Q
        else:
            small, large = Q, P
            
        neg_q = False
        for g in small.elements:
            if g.is_Identity:
                continue
            if large.contains(g):
                neg_q = True
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are distinct primes",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: Q is a Sylow q-subgroup of G",
    "¬Q: The intersection P \\cap Q is not the trivial subgroup {1}"
]

N_HYP = 3
NEG_Q_INDEX = 3
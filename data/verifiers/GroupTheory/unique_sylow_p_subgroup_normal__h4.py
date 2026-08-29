import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness):
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False
        
    try:
        if not isinstance(P, PermutationGroup) or int(p) != p or p <= 1:
            h3 = False
        else:
            p_int = int(p)
            is_sub = P.is_subgroup(G)
            order_G = G.order()
            order_P = P.order()
            
            k = 0
            temp = order_G
            while temp % p_int == 0:
                k += 1
                temp //= p_int
                
            h3 = bool(is_sub and (order_P == p_int**k))
    except Exception:
        h3 = False
        
    try:
        neg_q = bool(P.is_subgroup(G) and not P.is_normal(G))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3
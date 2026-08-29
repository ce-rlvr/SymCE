import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G, p, P, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False
        
    # H_3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        elif p <= 1:
            h3 = False
        else:
            is_sub = True
            for g in P.generators:
                if g not in G:
                    is_sub = False
                    break
            if not is_sub:
                h3 = False
            else:
                order_G = G.order()
                order_P = P.order()
                k = 0
                temp = order_G
                while temp % p == 0:
                    k += 1
                    temp //= p
                h3 = (order_P == p**k)
    except Exception:
        h3 = False
        
    # ¬Q: PN/N is not a Sylow p-subgroup of G/N
    try:
        if not isinstance(N, PermutationGroup):
            neg_q = True
        elif p <= 1:
            neg_q = True
        else:
            is_sub = True
            for g in N.generators:
                if g not in G:
                    is_sub = False
                    break
            if not is_sub:
                neg_q = True
            elif not N.is_normal(G):
                # If N is not normal, G/N is not a group, so PN/N cannot be a Sylow p-subgroup
                neg_q = True
            else:
                # If N is normal, we check if PN/N is a Sylow p-subgroup of G/N
                PN = PermutationGroup(list(P.generators) + list(N.generators))
                order_Q = G.order() // N.order()
                order_PN_N = PN.order() // N.order()
                
                k = 0
                temp = order_Q
                while temp % p == 0:
                    k += 1
                    temp //= p
                    
                if order_PN_N == p**k:
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = True
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: PN/N is not a Sylow p-subgroup of G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3
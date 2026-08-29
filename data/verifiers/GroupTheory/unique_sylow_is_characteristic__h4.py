import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.ntheory import isprime

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
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime dividing the order of G
    try:
        if not isprime(p):
            h2 = False
        else:
            h2 = (G.order() % p == 0)
    except Exception:
        h2 = False
        
    # H_3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        elif not all(g in G for g in P.generators):
            h3 = False
        elif not isprime(p):
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
        
    # neg_Q: P is not a characteristic subgroup of G
    try:
        if not isinstance(P, PermutationGroup) or not all(g in G for g in P.generators):
            neg_q = True
        else:
            # For a Sylow p-subgroup, being characteristic is equivalent to being normal.
            # Since a valid witness must be a Sylow p-subgroup, we can just check normality.
            is_normal = True
            for g in G.generators:
                for h in P.generators:
                    if (g * h * ~g) not in P:
                        is_normal = False
                        break
                    if (~g * h * g) not in P:
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = not is_normal
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime dividing the order of G",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: P is not a characteristic subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3
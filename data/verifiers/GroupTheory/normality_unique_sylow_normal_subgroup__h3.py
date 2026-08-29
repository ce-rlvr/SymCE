import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Standard group theory objects
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

def is_subgroup(sub, grp):
    if not isinstance(sub, PermutationGroup) or not isinstance(grp, PermutationGroup):
        return False
    for g in sub.generators:
        if g not in grp:
            return False
    return True

def is_normal(sub, grp):
    if not is_subgroup(sub, grp):
        return False
    for g in grp.generators:
        for h in sub.generators:
            if (g * h * ~g) not in sub:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        G, N, P, p = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    # H_3: P is the unique Sylow p-subgroup of N
    try:
        h3 = False
        if is_subgroup(N, G) and is_subgroup(P, N):
            if isinstance(p, (int, sympy.Integer)) and p > 1:
                n_order = N.order()
                p_order = P.order()
                
                k = 0
                temp = n_order
                while temp > 0 and temp % p == 0:
                    k += 1
                    temp //= p
                    
                if p_order == p**k:
                    # All Sylow p-subgroups are conjugate, so uniqueness is equivalent to normality
                    h3 = is_normal(P, N)
    except Exception:
        h3 = False
        
    # ¬Q: P is not a normal subgroup of G
    try:
        neg_q = not is_normal(P, G)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is the unique Sylow p-subgroup of N",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3
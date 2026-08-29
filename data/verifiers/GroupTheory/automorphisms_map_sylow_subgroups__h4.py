import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime

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

def conditions(witness) -> list[bool]:
    try:
        G, p, P, phi = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    # H3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        else:
            is_sub = True
            for g in P.generators:
                try:
                    if g not in G:
                        is_sub = False
                        break
                except Exception:
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
        
    # neg_Q: phi(P) is NOT a Sylow p-subgroup of G
    try:
        elements_P = list(P.generate())
        image_P = set()
        for x in elements_P:
            if callable(phi):
                y = phi(x)
            else:
                y = phi[x]
            image_P.add(y)
            
        order_G = G.order()
        k = 0
        temp = order_G
        while temp % p == 0:
            k += 1
            temp //= p
        target_order = p**k
        
        is_sylow = True
        if len(image_P) != target_order:
            is_sylow = False
        else:
            for a in image_P:
                try:
                    in_G = a in G
                except Exception:
                    in_G = False
                if not in_G:
                    is_sylow = False
                    break
                
                for b in image_P:
                    try:
                        prod = a * b
                    except Exception:
                        is_sylow = False
                        break
                    if prod not in image_P:
                        is_sylow = False
                        break
                if not is_sylow:
                    break
        neg_q = not is_sylow
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: The image phi(P) is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3
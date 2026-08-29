import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False
        
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    try:
        h3 = isinstance(P, PermutationGroup) and P.is_subgroup(G)
    except Exception:
        h3 = False
        
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            index = int(G.order()) // int(P.order())
            order_P = int(P.order())
            p_int = int(p)
            
            coprime = (math.gcd(index, p_int) == 1)
            
            is_power = False
            if order_P == 1:
                is_power = True
            else:
                temp = order_P
                while temp % p_int == 0:
                    temp //= p_int
                is_power = (temp == 1)
                
            neg_q = not (coprime and is_power)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a finite Galois extension",
    "H_2: G = Gal(E/F) is the Galois group of the extension",
    "H_3: E^P is the fixed field of P in E",
    "¬Q: extension degree of E^P over F is not coprime to p, or extension degree of E over E^P is not a power of p"
]

N_HYP = 3
NEG_Q_INDEX = 3
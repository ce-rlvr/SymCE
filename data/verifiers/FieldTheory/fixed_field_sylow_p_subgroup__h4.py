import math
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def conditions(witness):
    try:
        G, P, p = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: E/F is a finite Galois extension
    try:
        h1 = hasattr(G, 'order') and G.order() > 0
    except Exception:
        h1 = False
        
    # H_2: G = Gal(E/F) is the Galois group of the extension
    try:
        h2 = P.is_subgroup(G)
    except Exception:
        h2 = False
        
    # H_3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(p, (int, sympy.Integer)):
            h3 = False
        else:
            p_val = int(p)
            if p_val < 1:
                h3 = False
            else:
                order_G = G.order()
                order_P = P.order()
                if p_val == 1:
                    h3 = (order_P == 1)
                else:
                    max_k = 0
                    while order_G % (p_val**(max_k + 1)) == 0:
                        max_k += 1
                    h3 = (order_P == p_val**max_k)
    except Exception:
        h3 = False
        
    # neg_Q: The extension degree [E^P : F] is not coprime to p, or [E : E^P] is not a power of p
    try:
        p_val = int(p)
        order_G = G.order()
        order_P = P.order()
        index = order_G // order_P
        
        coprime = (math.gcd(index, p_val) == 1)
        
        n = order_P
        if n == 1:
            is_pow = True
        elif n == 0:
            is_pow = False
        elif p_val == 1:
            is_pow = (n == 1)
        elif p_val == 0:
            is_pow = False
        elif p_val == -1:
            is_pow = (n == 1 or n == -1)
        else:
            while n % p_val == 0:
                n //= p_val
            is_pow = (n == 1)
            
        q = coprime and is_pow
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: E/F is a finite Galois extension",
    "H_2: G is the Galois group of the extension",
    "H_3: P is a Sylow p-subgroup of G",
    "not Q: The extension degree of E^P over F is not coprime to p, or E over E^P is not a power of p"
]

N_HYP = 3
NEG_Q_INDEX = 3
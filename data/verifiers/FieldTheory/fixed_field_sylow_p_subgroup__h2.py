import math
from sympy import isprime
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def is_power_of(n, p):
    if n < 1:
        return False
    while n % p == 0:
        n //= p
    return n == 1

def get_val(witness, keys, default=None):
    if isinstance(witness, dict):
        for k in keys:
            if k in witness:
                return witness[k]
    else:
        for k in keys:
            if hasattr(witness, k):
                return getattr(witness, k)
    return default

def get_order(obj):
    if isinstance(obj, int):
        return obj
    if hasattr(obj, 'order'):
        if callable(obj.order):
            return obj.order()
        return obj.order
    return None

def conditions(witness) -> list[bool]:
    try:
        deg_E_F = int(get_val(witness, ['deg_E_F', 'E_F']))
        p = int(get_val(witness, ['p']))
        
        G = get_val(witness, ['G', 'group_G'])
        if G is not None:
            order_G = int(get_order(G))
        else:
            order_G = int(get_val(witness, ['order_G', 'G_order']))
            
        P = get_val(witness, ['P', 'group_P'])
        if P is not None:
            order_P = int(get_order(P))
        else:
            order_P = int(get_val(witness, ['order_P', 'P_order']))
            
        deg_E_EP = int(get_val(witness, ['deg_E_EP', 'E_EP']))
        deg_EP_F = int(get_val(witness, ['deg_EP_F', 'EP_F']))
    except Exception:
        return [False, False, False, False]

    # H1: E/F is a finite Galois extension
    try:
        is_galois = get_val(witness, ['is_galois'], True)
        h1 = (deg_E_F > 0) and bool(is_galois)
    except Exception:
        h1 = False

    # H2: P is a Sylow p-subgroup of G
    try:
        h2 = (isprime(p) and 
              order_G > 0 and 
              order_P > 0 and 
              order_G % order_P == 0 and 
              math.gcd(order_G // order_P, p) == 1 and 
              is_power_of(order_P, p))
    except Exception:
        h2 = False

    # H3: E^P is the fixed field of P in E
    try:
        h3 = (deg_E_F == deg_E_EP * deg_EP_F) and (deg_E_EP == order_P)
    except Exception:
        h3 = False

    # Conclusion: [E^P : F] is coprime to p, and [E : E^P] is a power of p
    try:
        q = (math.gcd(deg_EP_F, p) == 1) and is_power_of(deg_E_EP, p)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a finite Galois extension",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: E^P is the fixed field of P in E",
    "not Q: degree of E^P over F is not coprime to p, or degree of E over E^P is not a power of p"
]

N_HYP = 3
NEG_Q_INDEX = 3
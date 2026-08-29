import sympy
from sympy import ZZ as sympy_ZZ, QQ as sympy_QQ, RR as sympy_RR, CC as sympy_CC

# Top-level setup: named object bindings that the witness expression may reference.
class CustomRing:
    def __init__(self, is_commutative, is_trivial, is_euclidean):
        self.is_commutative = is_commutative
        self.is_trivial = is_trivial
        self.is_euclidean = is_euclidean

ZZ = CustomRing(True, False, True)
QQ = CustomRing(True, False, True)
RR = CustomRing(True, False, True)
CC = CustomRing(True, False, True)
Z0 = CustomRing(True, True, False)
zero_ring = Z0
trivial_ring = Z0
Z2 = CustomRing(True, False, True)
Z3 = CustomRing(True, False, True)
Z4 = CustomRing(True, False, False)
Z5 = CustomRing(True, False, True)
Z6 = CustomRing(True, False, False)

def get_ring_props(R):
    """
    Returns a tuple (is_commutative, is_trivial, is_euclidean) for a given ring.
    """
    if hasattr(R, 'is_commutative') and hasattr(R, 'is_trivial') and hasattr(R, 'is_euclidean'):
        return R.is_commutative, R.is_trivial, R.is_euclidean
    
    if isinstance(R, (int, sympy.Integer)):
        n = int(R)
        if n == 1:
            return True, True, False
        elif n == 0:
            return True, False, True
        else:
            is_prime = sympy.isprime(n)
            return True, False, is_prime
            
    if R in (sympy_ZZ, sympy_QQ, sympy_RR, sympy_CC):
        return True, False, True
        
    if isinstance(R, str):
        R_upper = R.upper()
        if R_upper in ('Z', 'ZZ', 'Q', 'QQ', 'R', 'RR', 'C', 'CC'):
            return True, False, True
        if R_upper in ('Z0', '0', 'TRIVIAL', 'ZERO'):
            return True, True, False
            
    raise ValueError("Unknown ring representation")

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        R1, R2 = witness
    except Exception:
        return [False, False]
        
    # H_1: R_1 is a non-trivial commutative ring
    try:
        c1, t1, e1 = get_ring_props(R1)
        h1_ok = c1 and not t1
    except Exception:
        h1_ok = False
        
    # ¬Q: The direct product R_1 x R_2 is a Euclidean domain
    try:
        c1, t1, e1 = get_ring_props(R1)
        c2, t2, e2 = get_ring_props(R2)
        
        # The direct product of two rings R1 x R2 is a Euclidean domain (which must be an integral domain)
        # if and only if exactly one of the rings is a Euclidean domain and the other is the trivial ring.
        # If both are non-trivial, the product has zero divisors (e.g., (1,0)*(0,1) = (0,0)).
        # If both are trivial, the product is trivial, and the trivial ring is not an integral domain.
        neg_q_ok = (e1 and t2) or (e2 and t1)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R_1 is a non-trivial commutative ring",
    "¬Q: The direct product R_1 x R_2 is a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1
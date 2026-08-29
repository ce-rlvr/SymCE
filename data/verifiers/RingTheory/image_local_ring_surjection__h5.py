import sympy
from sympy.ntheory import factorint

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12
QQ = sympy.QQ
ZZ = sympy.ZZ

def get_ring_n(R):
    if isinstance(R, int):
        return R
    if hasattr(R, 'order'):
        try:
            return int(R.order())
        except Exception:
            pass
    if hasattr(R, 'is_Integer') and R.is_Integer:
        return int(R)
    return None

def is_comm_ring_with_id(R):
    n = get_ring_n(R)
    if n is not None:
        return True
    if R in [sympy.QQ, sympy.ZZ]:
        return True
    return False

def is_zero_ring(R):
    n = get_ring_n(R)
    if n is not None:
        return abs(n) == 1
    return False

def is_local_ring(R):
    n = get_ring_n(R)
    if n is not None:
        if n == 0:
            return False
        if abs(n) == 1:
            return False
        return len(factorint(abs(n))) == 1
    if R == sympy.QQ:
        return True
    if R == sympy.ZZ:
        return False
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R, S = witness, None
    except Exception:
        R, S = None, None

    try:
        h1 = is_comm_ring_with_id(R)
    except Exception:
        h1 = False

    try:
        h2 = is_local_ring(R)
    except Exception:
        h2 = False

    try:
        h3 = is_comm_ring_with_id(S)
    except Exception:
        h3 = False

    try:
        h4 = is_comm_ring_with_id(S) and not is_zero_ring(S)
    except Exception:
        h4 = False

    try:
        neg_q = is_comm_ring_with_id(S) and not is_local_ring(S)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a local ring",
    "H_3: S is a commutative ring with identity",
    "H_4: S is not the zero ring",
    "¬Q: S is not a local ring"
]

N_HYP = 4
NEG_Q_INDEX = 4
import sympy
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.polys.domains import CC, QQ, RR, ZZ, GF

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_char(R):
    if hasattr(R, 'characteristic'):
        c = R.characteristic
        if callable(c):
            return c()
        return c
    if hasattr(R, 'char'):
        c = R.char
        if callable(c):
            return c()
        return c
    try:
        if R in (QQ, RR, CC):
            return 0
        if R.__class__.__name__ == 'GaloisField':
            return R.mod
        if R.__class__.__name__ == 'FractionField':
            return get_char(R.domain)
        if R.__class__.__name__ == 'AlgebraicField':
            return get_char(R.domain)
    except Exception:
        pass
    return None

def is_field(R):
    if hasattr(R, 'is_Field'):
        c = R.is_Field
        if callable(c):
            return c()
        return c
    if hasattr(R, 'is_field'):
        c = R.is_field
        if callable(c):
            return c()
        return c
    try:
        if R in (QQ, RR, CC):
            return True
        if R.__class__.__name__ == 'GaloisField':
            return True
        if R.__class__.__name__ == 'FractionField':
            return True
        if R.__class__.__name__ == 'AlgebraicField':
            return True
    except Exception:
        pass
    return False

def is_algebraically_closed(R):
    if hasattr(R, 'is_algebraically_closed'):
        c = R.is_algebraically_closed
        if callable(c):
            return c()
        return c
    try:
        if R == CC:
            return True
    except Exception:
        pass
    return False

def is_perfect_field(F):
    if not is_field(F):
        return False
    if hasattr(F, 'is_perfect'):
        c = F.is_perfect
        if callable(c):
            return c()
        return c
    char = get_char(F)
    if char == 0:
        return True
    if F.__class__.__name__ == 'GaloisField':
        return True
    if F.__class__.__name__ == 'FractionField':
        return False
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            K, L, F = witness
        elif isinstance(witness, dict):
            K = witness.get('K')
            L = witness.get('L')
            F = witness.get('F')
        elif hasattr(witness, 'K') and hasattr(witness, 'L') and hasattr(witness, 'F'):
            K = witness.K
            L = witness.L
            F = witness.F
        else:
            K, L, F = witness, witness, witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(is_field(K) and is_field(L))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_algebraically_closed(K) and is_algebraically_closed(L))
    except Exception:
        h2 = False

    try:
        h3 = bool(is_perfect_field(F))
    except Exception:
        h3 = False

    try:
        if hasattr(witness, 'is_reduced'):
            c = witness.is_reduced
            neg_q = not bool(c() if callable(c) else c)
        else:
            char_K = get_char(K)
            char_L = get_char(L)
            char_F = get_char(F)
            
            if char_K is None or char_L is None or char_F is None:
                neg_q = True
            elif char_K != char_F or char_L != char_F:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K and L are fields",
    "H_2: K and L are algebraically closed",
    "H_3: F is a perfect field",
    "¬Q: The tensor product K \\otimes_F L is not a reduced ring"
]

N_HYP = 3
NEG_Q_INDEX = 3
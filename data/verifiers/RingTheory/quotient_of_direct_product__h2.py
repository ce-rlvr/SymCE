import sympy
from sympy import S

# Top-level setup for Ring Theory
ZZ = S.Integers
QQ = S.Rationals
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def _get_ring_size(R):
    """
    Helper to interpret the ring R.
    Returns S.Integers for ZZ, or an integer n for Z/nZ.
    """
    if R == S.Integers:
        return S.Integers
    if isinstance(R, (int, sympy.Integer)) and R > 0:
        return int(R)
    if isinstance(R, (set, frozenset, tuple, list, sympy.FiniteSet)):
        try:
            s = set(R)
            if all(isinstance(x, (int, sympy.Integer)) for x in s):
                n = len(s)
                if s == set(range(n)):
                    return n
        except Exception:
            pass
    return None

def is_ideal(I, R):
    """
    Checks if I is an ideal of R.
    Supports R = ZZ and R = Z/nZ.
    """
    R_size = _get_ring_size(R)
    
    if R_size == S.Integers:
        # In ZZ, any integer represents a principal ideal.
        if isinstance(I, (int, sympy.Integer)):
            return True
        # A finite set is an ideal of ZZ iff it is {0}.
        if isinstance(I, (list, set, tuple, sympy.FiniteSet)):
            try:
                I_set = set(I)
            except Exception:
                return False
            if I_set == {0}:
                return True
            return False
        return False
        
    elif isinstance(R_size, int) and R_size > 0:
        # In Z/nZ, an integer represents a principal ideal.
        if isinstance(I, (int, sympy.Integer)):
            return True
        try:
            I_set = set(I)
        except Exception:
            return False
        if not I_set:
            return False
        if not I_set.issubset(set(range(R_size))):
            return False
        # Check closure under subtraction
        for a in I_set:
            for b in I_set:
                if (a - b) % R_size not in I_set:
                    return False
        # Check absorption under multiplication
        for r in range(R_size):
            for x in I_set:
                if (r * x) % R_size not in I_set:
                    return False
        return True
        
    return False

def conditions(witness) -> list[bool]:
    try:
        R1, R2, I1, I2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R_1 and R_2 are rings
    try:
        R1_size = _get_ring_size(R1)
        R2_size = _get_ring_size(R2)
        h1 = (R1_size is not None) and (R2_size is not None)
    except Exception:
        h1 = False
        
    # H_2: I_2 is an ideal of R_2
    try:
        h2 = is_ideal(I2, R2)
    except Exception:
        h2 = False
        
    # ¬Q: The quotient ring (R_1 x R_2) / (I_1 x I_2) is NOT isomorphic to (R_1 / I_1) x (R_2 / I_2)
    # The conclusion fails if either I1 or I2 is not an ideal, as the quotient ring would not be well-defined.
    try:
        neg_q = not (is_ideal(I1, R1) and is_ideal(I2, R2))
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R_1 and R_2 are rings",
    "H_2: I_2 is an ideal of R_2",
    "¬Q: The quotient ring (R_1 x R_2) / (I_1 x I_2) is not isomorphic to (R_1 / I_1) x (R_2 / I_2)"
]

N_HYP = 2
NEG_Q_INDEX = 2
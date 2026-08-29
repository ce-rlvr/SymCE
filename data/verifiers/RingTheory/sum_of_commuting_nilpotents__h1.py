import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer, Symbol, symbols

# Top-level setup: standard named objects
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: x and y are nilpotent elements of R",
    "H_2: x and y commute",
    "¬Q: The sum x + y is not a nilpotent element of R"
]

def is_nilpotent(z, max_power=1000):
    try:
        if hasattr(z, 'is_nilpotent'):
            res = z.is_nilpotent() if callable(z.is_nilpotent) else z.is_nilpotent
            if res is not None:
                return bool(res)
    except Exception:
        pass

    try:
        if hasattr(z, 'shape') and len(z.shape) == 2:
            max_power = max(max_power, z.shape[0])
    except Exception:
        pass

    try:
        zero = z * 0
    except Exception:
        try:
            zero = z - z
        except Exception:
            zero = 0

    curr = z
    for _ in range(max_power):
        try:
            eq = (curr == zero)
            if isinstance(eq, bool):
                if eq: return True
            else:
                if bool(eq): return True
        except Exception:
            pass
            
        try:
            if hasattr(curr, 'equals') and curr.equals(zero):
                return True
        except Exception:
            pass
            
        try:
            if hasattr(curr, 'is_zero') and curr.is_zero:
                return True
        except Exception:
            pass
        
        try:
            curr = curr * z
        except Exception:
            return False

    return False

def commutes(x, y):
    try:
        xy = x * y
        yx = y * x
    except Exception:
        return False

    try:
        eq = (xy == yx)
        if isinstance(eq, bool):
            if eq: return True
        else:
            if bool(eq): return True
    except Exception:
        pass

    try:
        if hasattr(xy, 'equals') and xy.equals(yx):
            return True
    except Exception:
        pass

    try:
        diff = xy - yx
        if hasattr(diff, 'is_zero') and diff.is_zero:
            return True
    except Exception:
        pass

    return False

def conditions(witness) -> list[bool]:
    try:
        x, y = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_nilpotent(x) and is_nilpotent(y)
    except Exception:
        h1 = False
        
    try:
        h2 = commutes(x, y)
    except Exception:
        h2 = False
        
    try:
        neg_q = not is_nilpotent(x + y)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]
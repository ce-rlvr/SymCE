import sympy
import math
from sympy.ntheory import factorint

class ZmodRing:
    """
    Represents the ring of integers modulo n (Z/nZ).
    """
    def __init__(self, n):
        self.n = int(n)
        
    def is_local(self):
        if self.n <= 1:
            return False
        # A finite commutative ring Z/nZ is local iff n is a prime power p^k
        f = factorint(self.n)
        return len(f) == 1
        
    def has_identity(self):
        return self.n > 1
        
    def maximal_ideal(self):
        if not self.is_local():
            return None
        f = factorint(self.n)
        p = list(f.keys())[0]
        return set(i for i in range(self.n) if i % p == 0)
        
    def is_unit(self, x):
        try:
            return math.gcd(int(x) % self.n, self.n) == 1
        except Exception:
            return False
            
    def __contains__(self, x):
        try:
            int(x)
            return True
        except Exception:
            return False
            
    def __eq__(self, other):
        return isinstance(other, ZmodRing) and self.n == other.n
        
    def __hash__(self):
        return hash(('ZmodRing', self.n))
        
    def __str__(self):
        return f"Z/{self.n}Z"
        
    def __repr__(self):
        return f"ZmodRing({self.n})"

# Named bindings for common local rings
Z2 = ZmodRing(2)
Z3 = ZmodRing(3)
Z4 = ZmodRing(4)
Z8 = ZmodRing(8)
Z9 = ZmodRing(9)

def check_local(R):
    if hasattr(R, 'is_local'):
        return R.is_local()
    if getattr(R, 'is_Field', False):
        return True
    if R in (sympy.QQ, sympy.RR, sympy.CC):
        return True
    return False

def check_has_identity(R):
    if hasattr(R, 'has_identity'):
        return R.has_identity()
    return True

def check_maximal_ideal(R, M):
    if hasattr(R, 'maximal_ideal'):
        expected = R.maximal_ideal()
        try:
            return set(M) == set(expected)
        except Exception:
            return M == expected
    if getattr(R, 'is_Field', False) or R in (sympy.QQ, sympy.RR, sympy.CC):
        try:
            return set(M) == {0} or set(M) == {getattr(R, 'zero', 0)}
        except Exception:
            return False
    return False

def check_unit(R, x):
    if hasattr(R, 'is_unit'):
        return R.is_unit(x)
    if getattr(R, 'is_Field', False) or R in (sympy.QQ, sympy.RR, sympy.CC):
        try:
            return x != 0 and x != getattr(R, 'zero', 0)
        except Exception:
            return False
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, M, x) or a dict with keys 'R', 'M', 'x'.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            M = witness.get('M')
            x = witness.get('x')
        else:
            R, M, x = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a local ring with identity
    try:
        h1 = bool(check_local(R) and check_has_identity(R))
    except Exception:
        h1 = False

    # H_2: M is the unique maximal ideal of R
    try:
        h2 = bool(check_maximal_ideal(R, M))
    except Exception:
        h2 = False

    # ¬Q: x is not a unit in R
    try:
        in_R = False
        if hasattr(R, '__contains__'):
            in_R = x in R
        else:
            in_R = True
            
        neg_q = bool(in_R and not check_unit(R, x))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a local ring with identity",
    "H_2: M is the unique maximal ideal of R",
    "¬Q: x is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2
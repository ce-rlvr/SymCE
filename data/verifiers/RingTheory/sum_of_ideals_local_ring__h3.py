import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math
from functools import reduce

# Top-level setup for potential witness expressions
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

def get_n(R):
    """Extract the integer n if R represents Z/nZ."""
    if isinstance(R, (int, sympy.Integer)):
        return int(R)
    if isinstance(R, (list, set, tuple)):
        try:
            R_ints = sorted([int(x) for x in R])
            n = len(R_ints)
            if n > 0 and R_ints == list(range(n)):
                return n
        except Exception:
            pass
    return None

def get_generator(n, I):
    """Find the generator of the ideal I in Z/nZ."""
    if isinstance(I, (int, sympy.Integer)):
        return math.gcd(int(I), int(n))
    if isinstance(I, (list, set, tuple)):
        if not I: 
            return int(n)
        try:
            I_ints = [int(x) for x in I]
            return reduce(math.gcd, I_ints, int(n))
        except Exception:
            return None
    return None

def is_local_ring(R):
    n = get_n(R)
    if n is not None:
        if n <= 1: 
            return False
        factors = factorint(n)
        # A finite ring Z/nZ is local iff n is a prime power
        return len(factors) == 1
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    return False

def is_ideal(R, I):
    n = get_n(R)
    if n is not None:
        return get_generator(n, I) is not None
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    return False

def is_R(R, I):
    n = get_n(R)
    if n is not None:
        g = get_generator(n, I)
        return g == 1
    if hasattr(R, 'is_Field') and R.is_Field:
        if I in [0, [0], {0}, (0,), []]:
            return False
        return True
    return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        R, I, J = witness
        
        try:
            h1 = is_local_ring(R)
        except Exception:
            h1 = False
            
        try:
            h2 = is_ideal(R, I) and is_ideal(R, J)
        except Exception:
            h2 = False
            
        try:
            neg_q = not is_R(R, I) and not is_R(R, J)
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative local ring",
    "H_2: I and J are ideals of R",
    "¬Q: I != R and J != R"
]

N_HYP = 2
NEG_Q_INDEX = 2
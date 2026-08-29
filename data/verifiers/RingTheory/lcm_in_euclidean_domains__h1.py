import math
import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

class Z_sqrt_minus_5:
    """
    Represents an element x + y*sqrt(-5) in the ring Z[sqrt(-5)].
    This is the standard counterexample ring for LCM existence.
    """
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        
    def __eq__(self, other):
        if isinstance(other, int):
            return self.x == other and self.y == 0
        if not isinstance(other, Z_sqrt_minus_5):
            return False
        return self.x == other.x and self.y == other.y
        
    def __hash__(self):
        return hash((self.x, self.y))
        
    def __add__(self, other):
        if isinstance(other, int):
            return Z_sqrt_minus_5(self.x + other, self.y)
        return Z_sqrt_minus_5(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):
        if isinstance(other, int):
            return Z_sqrt_minus_5(self.x - other, self.y)
        return Z_sqrt_minus_5(self.x - other.x, self.y - other.y)
        
    def __mul__(self, other):
        if isinstance(other, int):
            return Z_sqrt_minus_5(self.x * other, self.y * other)
        return Z_sqrt_minus_5(self.x * other.x - 5 * self.y * other.y, 
                              self.x * other.y + self.y * other.x)
                              
    def norm(self):
        return self.x**2 + 5 * self.y**2
        
    def divides(self, other):
        if isinstance(other, int):
            other = Z_sqrt_minus_5(other, 0)
        if self.x == 0 and self.y == 0:
            return other.x == 0 and other.y == 0
        real_part = other.x * self.x + 5 * other.y * self.y
        imag_part = other.y * self.x - other.x * self.y
        n = self.norm()
        return real_part % n == 0 and imag_part % n == 0

    def __str__(self):
        return f"{self.x} + {self.y}*sqrt(-5)"
        
    def __repr__(self):
        return str(self)

def is_nonzero(x):
    if isinstance(x, Z_sqrt_minus_5):
        return x.x != 0 or x.y != 0
    if hasattr(x, 'is_zero') and x.is_zero is not None:
        return not x.is_zero
    return x != 0

def exists_lcm(a, b):
    if isinstance(a, Z_sqrt_minus_5) and isinstance(b, Z_sqrt_minus_5):
        ab = a * b
        N_ab = ab.norm()
        if N_ab == 0:
            return True
            
        M = []
        limit_x = int(math.isqrt(N_ab)) + 1
        limit_y = int(math.isqrt(N_ab // 5)) + 1
        for x in range(-limit_x, limit_x + 1):
            for y in range(-limit_y, limit_y + 1):
                d = Z_sqrt_minus_5(x, y)
                if d.norm() > 0 and N_ab % d.norm() == 0:
                    if d.divides(ab) and a.divides(d) and b.divides(d):
                        M.append(d)
                        
        C = []
        for x in range(-20, 21):
            for y in range(-20, 21):
                z = Z_sqrt_minus_5(x, y)
                c = a * z
                if b.divides(c):
                    C.append(c)
                    
        for m in M:
            m_is_lcm = True
            for c in C:
                if not m.divides(c):
                    m_is_lcm = False
                    break
            if m_is_lcm:
                return True
        return False
        
    try:
        sympy.lcm(a, b)
        return True
    except Exception:
        return True

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                a, b = witness
            elif len(witness) == 3:
                _, a, b = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        h1 = bool(is_nonzero(a))
        h2 = bool(is_nonzero(b))
        
        neg_q = not exists_lcm(a, b)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: a is non-zero",
    "H_2: b is non-zero",
    "¬Q: There does not exist a least common multiple of a and b in R"
]

N_HYP = 2
NEG_Q_INDEX = 2
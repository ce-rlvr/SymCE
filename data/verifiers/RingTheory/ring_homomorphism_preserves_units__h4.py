import sympy
import math

def is_int(a):
    return isinstance(a, (int, sympy.Integer))

class CustomRing:
    def __init__(self, n):
        self.n = int(n)
        if self.n > 0:
            self.elements = list(range(self.n))
            
    @property
    def zero(self):
        return 0
        
    @property
    def one(self):
        return 1
        
    def add(self, a, b):
        a, b = int(a), int(b)
        return (a + b) % self.n if self.n > 0 else a + b
        
    def mul(self, a, b):
        a, b = int(a), int(b)
        return (a * b) % self.n if self.n > 0 else a * b
        
    def contains(self, a):
        if not is_int(a): 
            return False
        a = int(a)
        if self.n > 0:
            return 0 <= a < self.n
        return True
        
    def is_unit(self, a):
        if not self.contains(a): 
            return False
        a = int(a)
        if self.n > 0:
            return math.gcd(a, self.n) == 1
        return a in (1, -1)

ZZ = CustomRing(0)

def Zmod(n):
    return CustomRing(n)

def is_ring_with_identity(R):
    try:
        if not hasattr(R, 'zero') or not hasattr(R, 'one'): return False
        if not hasattr(R, 'add') or not hasattr(R, 'mul'): return False
        if not hasattr(R, 'contains') or not hasattr(R, 'is_unit'): return False
        if not R.contains(R.zero) or not R.contains(R.one): return False
        if R.add(R.zero, R.one) != R.one: return False
        if R.mul(R.one, R.one) != R.one: return False
        return True
    except Exception:
        return False

def is_homomorphism(f, R, S):
    try:
        if hasattr(R, 'elements'):
            test_elements = R.elements
        else:
            test_elements = [0, 1, -1, 2, -2, 3, -3, 10, -10]
            test_elements = [x for x in test_elements if R.contains(x)]
        
        for a in test_elements:
            for b in test_elements:
                fa = f(a)
                fb = f(b)
                if not S.contains(fa): return False
                if not S.contains(fb): return False
                if f(R.add(a, b)) != S.add(fa, fb): return False
                if f(R.mul(a, b)) != S.mul(fa, fb): return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            f = witness.get('f')
            u = witness.get('u')
        else:
            R, S, f, u = witness
    except Exception:
        return [False, False, False, False]

    # H1: R and S are rings with identity
    try:
        h1 = is_ring_with_identity(R) and is_ring_with_identity(S) and R.contains(u)
    except Exception:
        h1 = False

    # H2: f: R -> S is a ring homomorphism
    try:
        h2 = is_homomorphism(f, R, S)
    except Exception:
        h2 = False

    # H3: f maps the identity of R to the identity of S
    try:
        h3 = (f(R.one) == S.one)
    except Exception:
        h3 = False

    # neg_Q: f(u) is not a unit in S
    try:
        neg_q = not S.is_unit(f(u))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f: R -> S is a ring homomorphism",
    "H_3: f maps the identity of R to the identity of S",
    "¬Q: f(u) is not a unit in S"
]

N_HYP = 3
NEG_Q_INDEX = 3
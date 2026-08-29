import sympy
from sympy import ZZ, QQ

class CustomRing:
    def __init__(self, name):
        self.name = name
        self.zero = 0
        self.one = 1
        self.elements = list(range(-20, 21))
            
    def is_unit(self, a):
        if self.name == "Z":
            return a in (1, -1)
        if self.name == "Q":
            return a != 0
        return False
        
    def in_jacobson_radical(self, a):
        return a == 0
        
    def add(self, a, b):
        return a + b
        
    def mul(self, a, b):
        return a * b
        
    def eq(self, a, b):
        return a == b

    def __contains__(self, item):
        return item in self.elements

# Top-level setup: named object bindings that the witness expression may reference
Z_ring = CustomRing("Z")
Q_ring = CustomRing("Q")

def inclusion_map(x):
    return x

# Helper functions for the verifier
def is_ring(R):
    return hasattr(R, 'zero') and hasattr(R, 'one') and hasattr(R, 'is_unit')

def ring_add(R, a, b):
    try:
        if hasattr(R, 'add'): return R.add(a, b)
    except Exception:
        pass
    return a + b

def ring_mul(R, a, b):
    try:
        if hasattr(R, 'mul'): return R.mul(a, b)
    except Exception:
        pass
    return a * b

def ring_eq(R, a, b):
    try:
        if hasattr(R, 'eq'): return R.eq(a, b)
    except Exception:
        pass
    return a == b

def get_test_elements(R):
    if hasattr(R, 'elements'):
        return R.elements
    return list(range(-20, 21))

def in_jacobson_radical(R, a):
    try:
        if hasattr(R, 'in_jacobson_radical'):
            return R.in_jacobson_radical(a)
        if hasattr(R, 'jacobson_radical'):
            return a in R.jacobson_radical()
    except Exception:
        pass
    return ring_eq(R, a, R.zero)

def is_homomorphism(R, S, f):
    try:
        if not ring_eq(S, f(R.one), S.one):
            return False
        elems = get_test_elements(R)
        for a in elems:
            for b in elems:
                if not ring_eq(S, f(ring_add(R, a, b)), ring_add(S, f(a), f(b))):
                    return False
                if not ring_eq(S, f(ring_mul(R, a, b)), ring_mul(S, f(a), f(b))):
                    return False
        return True
    except Exception:
        return False

def ker_in_jacobson(R, S, f):
    try:
        elems = get_test_elements(R)
        for a in elems:
            if ring_eq(S, f(a), S.zero):
                if not in_jacobson_radical(R, a):
                    return False
        return True
    except Exception:
        return False

def in_ring(R, x):
    try:
        if hasattr(R, 'elements'):
            return x in R.elements
        if hasattr(R, '__contains__'):
            return x in R
    except Exception:
        pass
    return True

def conditions(witness) -> list[bool]:
    try:
        R, S, f, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: Let R and S be rings
    try:
        h1 = is_ring(R) and is_ring(S)
    except Exception:
        h1 = False
        
    # H_2: Let the kernel of f be contained in the Jacobson radical of R
    try:
        h2 = is_homomorphism(R, S, f) and ker_in_jacobson(R, S, f)
    except Exception:
        h2 = False
        
    # H_3: Let x be an element of R such that f(x) is a unit in S
    try:
        if not in_ring(R, x):
            h3 = False
        else:
            h3 = bool(S.is_unit(f(x)))
    except Exception:
        h3 = False
        
    # ¬Q: The element x is not a unit in R
    try:
        neg_q = not bool(R.is_unit(x))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: The kernel of f is contained in the Jacobson radical of R",
    "H_3: x is an element of R such that f(x) is a unit in S",
    "¬Q: The element x is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3
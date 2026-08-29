import itertools
import functools
import math
from sympy import symbols, Rational, Integer

# Top-level setup for potential witness expressions
class Z_n_ring:
    def __init__(self, n):
        self.elements = list(range(n))
        self.zero = 0
    def add(self, a, b):
        return (a + b) % len(self.elements)
    def mul(self, a, b):
        return (a * b) % len(self.elements)

Z2_ring = Z_n_ring(2)
Z3_ring = Z_n_ring(3)
Z4_ring = Z_n_ring(4)
Z6_ring = Z_n_ring(6)

class RingWrapper:
    def __init__(self, obj):
        if isinstance(obj, dict):
            self.elements = list(obj['elements'])
            self.add = obj['add']
            self.mul = obj['mul']
            self.zero = obj['zero']
        else:
            self.elements = list(obj.elements)
            self.add = obj.add
            self.mul = obj.mul
            self.zero = obj.zero

def is_ring(R):
    elements = R.elements
    zero = R.zero
    if zero not in elements:
        return False
        
    for a in elements:
        if R.add(a, zero) != a or R.add(zero, a) != a: 
            return False
        has_neg = False
        for b in elements:
            if R.add(a, b) == zero and R.add(b, a) == zero:
                has_neg = True
                break
        if not has_neg: 
            return False
        
        for b in elements:
            ab_add = R.add(a, b)
            if ab_add not in elements: return False
            ab_mul = R.mul(a, b)
            if ab_mul not in elements: return False
            if ab_add != R.add(b, a): return False
            
            for c in elements:
                if R.add(ab_add, c) != R.add(a, R.add(b, c)): return False
                if R.mul(ab_mul, c) != R.mul(a, R.mul(b, c)): return False
                if R.mul(a, R.add(b, c)) != R.add(ab_mul, R.mul(a, c)): return False
                if R.mul(R.add(a, b), c) != R.add(R.mul(a, c), R.mul(b, c)): return False
    return True

def is_boolean_ring(R):
    if not is_ring(R): 
        return False
    for a in R.elements:
        if R.mul(a, a) != a: 
            return False
    return True

def has_identity(R):
    for e in R.elements:
        is_id = True
        for a in R.elements:
            if R.mul(e, a) != a or R.mul(a, e) != a:
                is_id = False
                break
        if is_id:
            return True
    return False

def jacobson_radical(R):
    def sub(a, b):
        for c in R.elements:
            if R.add(b, c) == R.zero and R.add(c, b) == R.zero:
                return R.add(a, c)
        raise ValueError("No additive inverse")
        
    def is_rqr(a):
        for b in R.elements:
            ab = R.mul(a, b)
            term = sub(b, ab)
            if R.add(a, term) == R.zero:
                return True
        return False

    J = []
    for x in R.elements:
        x_in_J = True
        for y in R.elements:
            xy = R.mul(x, y)
            if not is_rqr(xy):
                x_in_J = False
                break
        if x_in_J:
            J.append(x)
    return J

def conditions(witness):
    try:
        R = RingWrapper(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_boolean_ring(R)
    except Exception:
        h1 = False
        
    try:
        h2 = has_identity(R)
    except Exception:
        h2 = False
        
    try:
        J = jacobson_radical(R)
        neg_q = False
        for x in J:
            if x != R.zero:
                neg_q = True
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: R has a multiplicative identity",
    "¬Q: J != {0}"
]

N_HYP = 2
NEG_Q_INDEX = 2
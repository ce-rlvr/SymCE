import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

class Ring:
    def __init__(self, elements, add, mul, zero, one=None):
        self.elements = list(elements)
        self.add = add
        self.mul = mul
        self.zero = zero
        self.one = one

Z2 = Ring([0, 1], lambda x, y: (x+y)%2, lambda x, y: (x*y)%2, 0, 1)
Z3 = Ring([0, 1, 2], lambda x, y: (x+y)%3, lambda x, y: (x*y)%3, 0, 1)
Z4 = Ring([0, 1, 2, 3], lambda x, y: (x+y)%4, lambda x, y: (x*y)%4, 0, 1)
Z5 = Ring([0, 1, 2, 3, 4], lambda x, y: (x+y)%5, lambda x, y: (x*y)%5, 0, 1)
Z6 = Ring([0, 1, 2, 3, 4, 5], lambda x, y: (x+y)%6, lambda x, y: (x*y)%6, 0, 1)

def check_ring(R):
    try:
        elements = R.elements
        zero = R.zero
        for a in elements:
            for b in elements:
                if R.add(a, b) not in elements: return False
                if R.add(a, b) != R.add(b, a): return False
                if R.mul(a, b) not in elements: return False
        for a in elements:
            if R.add(a, zero) != a: return False
        for a in elements:
            if not any(R.add(a, b) == zero for b in elements): return False
        for a in elements:
            for b in elements:
                for c in elements:
                    if R.add(R.add(a, b), c) != R.add(a, R.add(b, c)): return False
                    if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)): return False
                    if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): return False
                    if R.mul(R.add(a, b), c) != R.add(R.mul(a, c), R.mul(b, c)): return False
        if hasattr(R, 'one') and R.one is not None:
            for a in elements:
                if R.mul(a, R.one) != a: return False
                if R.mul(R.one, a) != a: return False
        return True
    except Exception:
        return False

def check_homomorphism(R, S, f):
    try:
        if isinstance(f, (dict, list, tuple)):
            func = lambda x: f[x]
        else:
            func = f
        
        for a in R.elements:
            if func(a) not in S.elements: return False
            for b in R.elements:
                if func(R.add(a, b)) != S.add(func(a), func(b)): return False
                if func(R.mul(a, b)) != S.mul(func(a), func(b)): return False
        
        if hasattr(R, 'one') and R.one is not None and hasattr(S, 'one') and S.one is not None:
            if func(R.one) != S.one: return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    """
    witness is expected to be a tuple: (R, S, f, e)
    where R and S are rings, f is a ring homomorphism from R to S,
    and e is an element of R.
    """
    try:
        R, S, f, e = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = check_ring(R) and check_ring(S) and (e in R.elements)
    except Exception:
        h1 = False
        
    try:
        h2 = check_homomorphism(R, S, f)
    except Exception:
        h2 = False
        
    try:
        if isinstance(f, (dict, list, tuple)):
            fe = f[e]
        else:
            fe = f(e)
        neg_q = (S.mul(fe, fe) != fe)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a ring homomorphism",
    "¬Q: f(e) is not an idempotent element in S"
]

N_HYP = 2
NEG_Q_INDEX = 2
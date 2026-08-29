import sympy
from sympy.matrices import eye, zeros
import math
import itertools
import functools

class Zn:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
    def add(self, a, b):
        return (a + b) % self.n
    def mul(self, a, b):
        return (a * b) % self.n

class DualZn:
    def __init__(self, n):
        self.n = n
        self.elements = [(a, b) for a in range(n) for b in range(n)]
    def add(self, x, y):
        return ((x[0] + y[0]) % self.n, (x[1] + y[1]) % self.n)
    def mul(self, x, y):
        return ((x[0] * y[0]) % self.n, (x[0] * y[1] + x[1] * y[0]) % self.n)

class ProductRing:
    def __init__(self, R1, R2):
        self.R1 = R1
        self.R2 = R2
        self.elements = [(a, b) for a in R1.elements for b in R2.elements]
    def add(self, x, y):
        return (self.R1.add(x[0], y[0]), self.R2.add(x[1], y[1]))
    def mul(self, x, y):
        return (self.R1.mul(x[0], y[0]), self.R2.mul(x[1], y[1]))

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_ring(R):
    try:
        elements = list(R.elements)
        add = R.add
        mul = R.mul
        if not elements: return False
        
        for a in elements:
            for b in elements:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
                
        for a in elements:
            for b in elements:
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                    
        for a in elements:
            for b in elements:
                if add(a, b) != add(b, a): return False
                
        zeros_list = []
        for z in elements:
            if all(add(z, a) == a and add(a, z) == a for a in elements):
                zeros_list.append(z)
        if len(zeros_list) != 1: return False
        z = zeros_list[0]
        
        for a in elements:
            if not any(add(a, b) == z and add(b, a) == z for b in elements): return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R1 = witness['R1']
            R2 = witness['R2']
            R = witness['R']
            e1 = witness['e1']
            e2 = witness['e2']
        else:
            R1, R2, R, e1, e2 = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_ring(R1) and is_ring(R2)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ring(R) and ((e1, e2) in R.elements)
    except Exception:
        h2 = False
        
    try:
        e1_idemp = (e1 in R1.elements) and (R1.mul(e1, e1) == e1)
        e2_idemp = (e2 in R2.elements) and (R2.mul(e2, e2) == e2)
        rhs = e1_idemp and e2_idemp
        
        e_tuple = (e1, e2)
        lhs = (e_tuple in R.elements) and (R.mul(e_tuple, e_tuple) == e_tuple)
        
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R1 and R2 are rings",
    "H_2: (e1, e2) is an element of R",
    "¬Q: (e1, e2) is idempotent in R iff e1 is idempotent in R1 and e2 is idempotent in R2 is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2
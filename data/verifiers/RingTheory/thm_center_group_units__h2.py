import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z
import itertools
import functools
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a unital ring",
    "H_2: Z(R) denotes the center of the ring R",
    "¬Q: Z(U(R)) is not equal to U(Z(R))"
]

N_HYP = 2
NEG_Q_INDEX = 2

class RingWrapper:
    def __init__(self, witness):
        if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
            self.elements = list(witness.elements)
            self.add = witness.add
            self.mul = witness.mul
            self.eq = getattr(witness, 'eq', lambda a, b: a == b)
            self.zero = getattr(witness, 'zero', None)
            self.one = getattr(witness, 'one', None)
        else:
            self.elements = list(witness)
            self.add = lambda a, b: a + b
            self.mul = lambda a, b: a * b
            self.eq = lambda a, b: a == b
            self.zero = None
            self.one = None

        if self.zero is None:
            for e in self.elements:
                try:
                    if all(self.eq(self.add(x, e), x) and self.eq(self.add(e, x), x) for x in self.elements):
                        self.zero = e
                        break
                except Exception:
                    pass
        if self.one is None:
            for e in self.elements:
                try:
                    if all(self.eq(self.mul(x, e), x) and self.eq(self.mul(e, x), x) for x in self.elements):
                        self.one = e
                        break
                except Exception:
                    pass

def check_H1(ring):
    if not ring.elements: 
        return False
    if ring.zero is None or ring.one is None: 
        return False
    n = len(ring.elements)
    if n > 100: 
        return False
    
    elements = ring.elements
    add = ring.add
    mul = ring.mul
    eq = ring.eq
    zero = ring.zero
    
    for a in elements:
        has_inv = False
        for b in elements:
            if eq(add(a, b), zero) and eq(add(b, a), zero):
                has_inv = True
                break
        if not has_inv: 
            return False
        
        for b in elements:
            s = add(a, b)
            p = mul(a, b)
            if not any(eq(s, x) for x in elements): return False
            if not any(eq(p, x) for x in elements): return False
            if not eq(s, add(b, a)): return False
            
            for c in elements:
                if not eq(add(s, c), add(a, add(b, c))): return False
                if not eq(mul(p, c), mul(a, mul(b, c))): return False
                if not eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))): return False
                if not eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))): return False
    return True

def check_neg_Q(ring):
    if ring.one is None:
        return False
        
    elements = ring.elements
    mul = ring.mul
    eq = ring.eq
    one = ring.one
    
    units = []
    for a in elements:
        for b in elements:
            if eq(mul(a, b), one) and eq(mul(b, a), one):
                units.append(a)
                break
                
    Z_U_R = []
    for u in units:
        is_central = True
        for v in units:
            if not eq(mul(u, v), mul(v, u)):
                is_central = False
                break
        if is_central:
            Z_U_R.append(u)
            
    Z_R = []
    for a in elements:
        is_central = True
        for x in elements:
            if not eq(mul(a, x), mul(x, a)):
                is_central = False
                break
        if is_central:
            Z_R.append(a)
            
    U_Z_R = []
    for a in Z_R:
        for b in Z_R:
            if eq(mul(a, b), one) and eq(mul(b, a), one):
                U_Z_R.append(a)
                break
                
    for a in Z_U_R:
        if not any(eq(a, b) for b in U_Z_R):
            return True
            
    for a in U_Z_R:
        if not any(eq(a, b) for b in Z_U_R):
            return True
            
    return False

def conditions(witness):
    try:
        ring = RingWrapper(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_H1(ring)
    except Exception:
        h1 = False
        
    # H2 is definitional
    h2 = True
    
    try:
        neg_q = check_neg_Q(ring)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]
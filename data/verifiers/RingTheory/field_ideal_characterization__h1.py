import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

class FiniteRing:
    """
    Helper class to easily construct finite rings for witnesses.
    elements: list of elements
    add_table: 2D list where add_table[i][j] is the index of elements[i] + elements[j]
    mul_table: 2D list where mul_table[i][j] is the index of elements[i] * elements[j]
    """
    def __init__(self, elements, add_table, mul_table, zero_idx=0):
        self.elements = elements
        self.add_table = add_table
        self.mul_table = mul_table
        self.zero = elements[zero_idx]
    
    def add(self, a, b):
        i = self.elements.index(a)
        j = self.elements.index(b)
        return self.elements[self.add_table[i][j]]

    def mul(self, a, b):
        i = self.elements.index(a)
        j = self.elements.index(b)
        return self.elements[self.mul_table[i][j]]

def get_elements(w):
    if hasattr(w, 'elements'): return w.elements
    return w[0]

def get_zero(w):
    if hasattr(w, 'zero'): return w.zero
    return w[3]

def add(w, a, b):
    if hasattr(w, 'add'): return w.add(a, b)
    return w[1][(a, b)]

def mul(w, a, b):
    if hasattr(w, 'mul'): return w.mul(a, b)
    return w[2][(a, b)]

def eq(x, y):
    return bool(x == y)

def is_ring(w):
    elements = get_elements(w)
    zero = get_zero(w)
    
    has_zero = False
    for e in elements:
        if eq(e, zero):
            has_zero = True
            break
    if not has_zero: return False
    
    for a in elements:
        if not eq(add(w, a, zero), a) or not eq(add(w, zero, a), a): return False
        
        has_inv = False
        for b in elements:
            if eq(add(w, a, b), zero) and eq(add(w, b, a), zero):
                has_inv = True
                break
        if not has_inv: return False
        
        for b in elements:
            ab_add = add(w, a, b)
            if not any(eq(ab_add, e) for e in elements): return False
            if not eq(ab_add, add(w, b, a)): return False
            
            ab_mul = mul(w, a, b)
            if not any(eq(ab_mul, e) for e in elements): return False
            
            for c in elements:
                if not eq(add(w, ab_add, c), add(w, a, add(w, b, c))): return False
                if not eq(mul(w, ab_mul, c), mul(w, a, mul(w, b, c))): return False
                if not eq(mul(w, a, add(w, b, c)), add(w, ab_mul, mul(w, a, c))): return False
                if not eq(mul(w, add(w, a, b), c), add(w, mul(w, a, c), mul(w, b, c))): return False
    return True

def ideal_generated_by(w, x):
    elements = get_elements(w)
    zero = get_zero(w)
    
    I = []
    def add_to_I(item):
        for y in I:
            if eq(y, item):
                return False
        I.append(item)
        return True

    add_to_I(x)
    add_to_I(zero)
    
    changed = True
    while changed:
        changed = False
        n = len(I)
        for i in range(n):
            for j in range(n):
                if add_to_I(add(w, I[i], I[j])):
                    changed = True
        for i in range(n):
            for r in elements:
                if add_to_I(mul(w, r, I[i])):
                    changed = True
                if add_to_I(mul(w, I[i], r)):
                    changed = True
        for i in range(n):
            for b in elements:
                if eq(add(w, I[i], b), zero):
                    if add_to_I(b):
                        changed = True
                    break
    return I

def has_two_ideals(w):
    elements = get_elements(w)
    zero = get_zero(w)
    
    unique_elements = []
    for e in elements:
        if not any(eq(e, u) for u in unique_elements):
            unique_elements.append(e)
            
    if len(unique_elements) < 2:
        return False
        
    for x in unique_elements:
        if eq(x, zero): continue
        I = ideal_generated_by(w, x)
        if len(I) != len(unique_elements):
            return False
    return True

def is_field(w):
    elements = get_elements(w)
    zero = get_zero(w)
    
    for a in elements:
        for b in elements:
            if not eq(mul(w, a, b), mul(w, b, a)):
                return False
                
    identity = None
    for e in elements:
        is_id = True
        for a in elements:
            if not eq(mul(w, e, a), a) or not eq(mul(w, a, e), a):
                is_id = False
                break
        if is_id:
            identity = e
            break
            
    if identity is None or eq(identity, zero):
        return False
        
    for a in elements:
        if eq(a, zero): continue
        has_inv = False
        for b in elements:
            if eq(mul(w, a, b), identity) and eq(mul(w, b, a), identity):
                has_inv = True
                break
        if not has_inv:
            return False
            
    return True

def conditions(witness):
    try:
        h1 = is_ring(witness) and has_two_ideals(witness)
    except Exception:
        h1 = False
        
    try:
        if not is_ring(witness):
            neg_q = False
        else:
            neg_q = not is_field(witness)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R has exactly two distinct ideals",
    "¬Q: R is not a field"
]

N_HYP = 1
NEG_Q_INDEX = 1
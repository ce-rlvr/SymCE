import operator
import itertools
import functools
import math
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

class RingZn:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
    def add(self, a, b): return (a + b) % self.n
    def mul(self, a, b): return (a * b) % self.n

Z2_ring = RingZn(2)
Z3_ring = RingZn(3)
Z4_ring = RingZn(4)
Z6_ring = RingZn(6)

def get_attr_or_key(obj, key):
    if isinstance(obj, dict) and key in obj:
        return obj[key]
    if hasattr(obj, key):
        return getattr(obj, key)
    raise KeyError(key)

def get_elements(R, domain=None):
    if callable(R) and domain is not None:
        raw = [elem for elem in domain if R(elem)]
    elif isinstance(R, dict) and 'elements' in R:
        raw = list(R['elements'])
    elif hasattr(R, 'elements'):
        if callable(R.elements):
            raw = list(R.elements())
        else:
            raw = list(R.elements)
    elif isinstance(R, (set, list, tuple)):
        raw = list(R)
    else:
        raise ValueError("Cannot get elements")
        
    unique = []
    for val in raw:
        if val not in unique:
            unique.append(val)
    return unique

def get_add(R):
    if isinstance(R, dict) and 'add' in R: return R['add']
    if hasattr(R, 'add'): return R.add
    return operator.add

def get_mul(R):
    if isinstance(R, dict) and 'mul' in R: return R['mul']
    if hasattr(R, 'mul'): return R.mul
    return operator.mul

def is_ring(R):
    try:
        elements = get_elements(R)
        add = get_add(R)
        mul = get_mul(R)
        
        if not elements: return False
        if len(elements) > 200: return False
        
        # closure
        for a in elements:
            for b in elements:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
                
        # associativity and distributivity
        for a in elements:
            for b in elements:
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                    
        # commutativity of add
        for a in elements:
            for b in elements:
                if add(a, b) != add(b, a): return False
                
        # zero
        zeros = [z_elem for z_elem in elements if all(add(z_elem, a) == a and add(a, z_elem) == a for a in elements)]
        if len(zeros) != 1: return False
        zero = zeros[0]
        
        # inverses
        for a in elements:
            if not any(add(a, b) == zero and add(b, a) == zero for b in elements):
                return False
                
        # one
        ones = [o for o in elements if all(mul(o, a) == a and mul(a, o) == a for a in elements)]
        if len(ones) != 1: return False
        
        return True
    except Exception:
        return False

def is_ring_homomorphism(f, R, S):
    try:
        R_elems = get_elements(R)
        S_elems = get_elements(S)
        R_add = get_add(R)
        R_mul = get_mul(R)
        S_add = get_add(S)
        S_mul = get_mul(S)
        
        def eval_f(val):
            if isinstance(f, dict): return f[val]
            return f(val)
            
        for a in R_elems:
            if eval_f(a) not in S_elems: return False
            
        for a in R_elems:
            for b in R_elems:
                if eval_f(R_add(a, b)) != S_add(eval_f(a), eval_f(b)): return False
                if eval_f(R_mul(a, b)) != S_mul(eval_f(a), eval_f(b)): return False
                
        R_ones = [o for o in R_elems if all(R_mul(o, a) == a and R_mul(a, o) == a for a in R_elems)]
        S_ones = [o for o in S_elems if all(S_mul(o, a) == a and S_mul(a, o) == a for a in S_elems)]
        if not R_ones or not S_ones: return False
        if eval_f(R_ones[0]) != S_ones[0]: return False
        
        return True
    except Exception:
        return False

def is_subring(E, R):
    try:
        R_elems = get_elements(R)
        R_add = get_add(R)
        R_mul = get_mul(R)
        
        try:
            E_elems = get_elements(E, domain=R_elems)
        except Exception:
            E_elems = get_elements(E)
            
        if not E_elems: return False
        
        for a in E_elems:
            if a not in R_elems: return False
            
        for a in E_elems:
            for b in E_elems:
                if R_add(a, b) not in E_elems: return False
                if R_mul(a, b) not in E_elems: return False
                
        R_zeros = [z_elem for z_elem in R_elems if all(R_add(z_elem, a) == a and R_add(a, z_elem) == a for a in R_elems)]
        R_ones = [o for o in R_elems if all(R_mul(o, a) == a and R_mul(a, o) == a for a in R_elems)]
        
        if not R_zeros or not R_ones: return False
        if R_zeros[0] not in E_elems: return False
        if R_ones[0] not in E_elems: return False
        
        for a in E_elems:
            has_inv = False
            for b in E_elems:
                if R_add(a, b) == R_zeros[0] and R_add(b, a) == R_zeros[0]:
                    has_inv = True
                    break
            if not has_inv: return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        R = get_attr_or_key(witness, 'R')
        S = get_attr_or_key(witness, 'S')
        f = get_attr_or_key(witness, 'f')
        g = get_attr_or_key(witness, 'g')
        E = get_attr_or_key(witness, 'E')
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_ring(R) and is_ring(S)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ring_homomorphism(f, R, S) and is_ring_homomorphism(g, R, S)
    except Exception:
        h2 = False
        
    try:
        neg_q = not is_subring(E, R)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S and g: R -> S are ring homomorphisms",
    "¬Q: E is not a subring of R"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import Rational, Integer
import itertools
import functools

# Top-level setup
# No specific named objects are required for this ring theory conjecture.
# The witness is expected to provide the ring elements and operations explicitly.

def extract(witness, key):
    if isinstance(witness, dict):
        return witness[key]
    return getattr(witness, key)

def parse_ring(ring_obj):
    if isinstance(ring_obj, dict):
        return (
            ring_obj['elements'],
            ring_obj['add'],
            ring_obj['mul'],
            ring_obj['zero'],
            ring_obj['one']
        )
    elif hasattr(ring_obj, 'elements'):
        return (
            ring_obj.elements,
            ring_obj.add,
            ring_obj.mul,
            ring_obj.zero,
            ring_obj.one
        )
    else:
        return ring_obj

def make_callable(op, elements):
    if isinstance(op, dict):
        return lambda a, b: op.get((a, b), None)
    elif isinstance(op, list):
        idx = {e: i for i, e in enumerate(elements)}
        return lambda a, b: op[idx[a]][idx[b]] if a in idx and b in idx else None
    return op

def make_callable_1(op, elements):
    if isinstance(op, dict):
        return lambda a: op.get(a, None)
    elif isinstance(op, list):
        idx = {e: i for i, e in enumerate(elements)}
        return lambda a: op[idx[a]] if a in idx else None
    return op

def is_ring_with_identity(elements, add, mul, zero, one):
    if zero not in elements or one not in elements:
        return False
    add_f = make_callable(add, elements)
    mul_f = make_callable(mul, elements)
    
    for a in elements:
        if add_f(a, zero) != a or add_f(zero, a) != a: return False
        if mul_f(a, one) != a or mul_f(one, a) != a: return False
        
        has_inv = False
        for b in elements:
            if add_f(a, b) == zero and add_f(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
        for b in elements:
            ab_add = add_f(a, b)
            ab_mul = mul_f(a, b)
            if ab_add not in elements: return False
            if ab_mul not in elements: return False
            
            if add_f(a, b) != add_f(b, a): return False
            
            for c in elements:
                if add_f(ab_add, c) != add_f(a, add_f(b, c)): return False
                if mul_f(ab_mul, c) != mul_f(a, mul_f(b, c)): return False
                if mul_f(a, add_f(b, c)) != add_f(ab_mul, mul_f(a, c)): return False
                if mul_f(ab_add, c) != add_f(mul_f(a, c), mul_f(b, c)): return False
                
    return True

def is_ring_homomorphism(elements_R, add_R, mul_R, elements_S, add_S, mul_S, f):
    f_c = make_callable_1(f, elements_R)
    add_R_c = make_callable(add_R, elements_R)
    mul_R_c = make_callable(mul_R, elements_R)
    add_S_c = make_callable(add_S, elements_S)
    mul_S_c = make_callable(mul_S, elements_S)
    
    for a in elements_R:
        fa = f_c(a)
        if fa not in elements_S: return False
        for b in elements_R:
            fb = f_c(b)
            if f_c(add_R_c(a, b)) != add_S_c(fa, fb): return False
            if f_c(mul_R_c(a, b)) != mul_S_c(fa, fb): return False
    return True

def is_unit(elements, mul, one, u):
    if u not in elements: return False
    mul_c = make_callable(mul, elements)
    for v in elements:
        if mul_c(u, v) == one and mul_c(v, u) == one:
            return True
    return False

def conditions(witness):
    try:
        R_obj = extract(witness, 'R')
        S_obj = extract(witness, 'S')
        f = extract(witness, 'f')
        u = extract(witness, 'u')
        
        R_elements, R_add, R_mul, R_zero, R_one = parse_ring(R_obj)
        S_elements, S_add, S_mul, S_zero, S_one = parse_ring(S_obj)
        
        R_elements = list(R_elements)
        S_elements = list(S_elements)
        
        if len(R_elements) > 50 or len(S_elements) > 50:
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = is_ring_with_identity(R_elements, R_add, R_mul, R_zero, R_one) and \
             is_ring_with_identity(S_elements, S_add, S_mul, S_zero, S_one)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ring_homomorphism(R_elements, R_add, R_mul, S_elements, S_add, S_mul, f)
    except Exception:
        h2 = False
        
    try:
        h3 = is_unit(R_elements, R_mul, R_one, u)
    except Exception:
        h3 = False
        
    try:
        f_c = make_callable_1(f, R_elements)
        fu = f_c(u)
        neg_q = not is_unit(S_elements, S_mul, S_one, fu)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f: R -> S is a ring homomorphism",
    "H_3: u is a unit in R",
    "¬Q: f(u) is not a unit in S"
]

N_HYP = 3
NEG_Q_INDEX = 3
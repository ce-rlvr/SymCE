import sympy
from sympy import symbols, Rational, Integer
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
ZZ = sympy.ZZ
QQ = sympy.QQ
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def is_infinite_ring(R):
    try:
        return R is sympy.ZZ or R is sympy.QQ
    except Exception:
        return False

def is_int_ring(R):
    return type(R) is int and R > 1

def get_ring_elements(R):
    if is_int_ring(R):
        return list(range(R))
    elif isinstance(R, dict) and 'elements' in R:
        return list(R['elements'])
    elif is_infinite_ring(R):
        return list(range(-100, 101))
    else:
        raise ValueError("Unsupported ring format")

def ring_add(R, x, y):
    if is_int_ring(R):
        return (x + y) % R
    elif isinstance(R, dict):
        return R['add'](x, y)
    elif is_infinite_ring(R):
        return x + y
    raise ValueError("Unsupported ring format")

def ring_mul(R, x, y):
    if is_int_ring(R):
        return (x * y) % R
    elif isinstance(R, dict):
        return R['mul'](x, y)
    elif is_infinite_ring(R):
        return x * y
    raise ValueError("Unsupported ring format")

def ring_zero(R):
    if is_int_ring(R):
        return 0
    elif isinstance(R, dict):
        return R['zero']
    elif is_infinite_ring(R):
        return 0
    raise ValueError("Unsupported ring format")

def ring_one(R):
    if is_int_ring(R):
        return 1
    elif isinstance(R, dict):
        return R['one']
    elif is_infinite_ring(R):
        return 1
    raise ValueError("Unsupported ring format")

def is_ring(R):
    if is_infinite_ring(R):
        return True
    try:
        if is_int_ring(R):
            return True
        
        elements = R['elements']
        add = R['add']
        mul = R['mul']
        zero = R['zero']
        one = R['one']
        
        if zero not in elements or one not in elements: 
            return False
        
        for a in elements:
            if add(a, zero) != a: return False
            if add(zero, a) != a: return False
            if mul(a, one) != a: return False
            if mul(one, a) != a: return False
            
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in elements:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
                if add(a, b) != add(b, a): return False
                
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        return True
    except Exception:
        return False

def apply_func(f, x):
    if callable(f):
        return f(x)
    elif isinstance(f, (dict, list, tuple)):
        return f[x]
    else:
        raise ValueError("Function must be callable, dict, list, or tuple")

def is_ring_hom(f, R, S):
    try:
        R_elems = get_ring_elements(R)
        
        for x in R_elems:
            fx = apply_func(f, x)
            if not is_infinite_ring(S) and fx not in get_ring_elements(S): 
                return False
            for y in R_elems:
                fy = apply_func(f, y)
                if apply_func(f, ring_add(R, x, y)) != ring_add(S, fx, fy): return False
                if apply_func(f, ring_mul(R, x, y)) != ring_mul(S, fx, fy): return False
        if apply_func(f, ring_one(R)) != ring_one(S): return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        R = witness['R']
        S_i = witness['S_i']
        f_i = witness['f_i']
        f = witness['f']
    except Exception:
        return [False, False, False, False]
        
    # H1: R is a ring
    try:
        h1 = is_ring(R)
    except Exception:
        h1 = False
        
    # H2: S_i is a family of rings
    try:
        h2 = isinstance(S_i, (list, tuple)) and all(is_ring(S) for S in S_i)
    except Exception:
        h2 = False
        
    # H3: f_i are ring homomorphisms
    try:
        h3 = isinstance(f_i, (list, tuple)) and len(f_i) == len(S_i) and all(is_ring_hom(fi, R, S) for fi, S in zip(f_i, S_i))
    except Exception:
        h3 = False
        
    # neg_Q: ker(f) != intersection of ker(f_i)
    try:
        R_elems = get_ring_elements(R)
        r_zero = ring_zero(R)
        
        if 'f_zero' in witness:
            f_zero = witness['f_zero']
        elif 'f_codomain' in witness:
            f_zero = ring_zero(witness['f_codomain'])
        else:
            f_zero = apply_func(f, r_zero)
            
        ker_f = set()
        for i, x in enumerate(R_elems):
            if apply_func(f, x) == f_zero:
                ker_f.add(i)
                
        ker_fi_list = []
        for fi, S in zip(f_i, S_i):
            ker = set()
            szero = ring_zero(S)
            for i, x in enumerate(R_elems):
                if apply_func(fi, x) == szero:
                    ker.add(i)
            ker_fi_list.append(ker)
            
        if ker_fi_list:
            inter_ker = set.intersection(*ker_fi_list)
        else:
            inter_ker = set(range(len(R_elems)))
            
        neg_q = (ker_f != inter_ker)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: {S_i} is a family of rings",
    "H_3: For each i, f_i is a ring homomorphism",
    "¬Q: The kernel of f is NOT the intersection of ker(f_i)"
]

N_HYP = 3
NEG_Q_INDEX = 3
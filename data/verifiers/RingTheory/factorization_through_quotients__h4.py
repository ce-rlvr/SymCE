import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z
import itertools
import functools
import math

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_ring_parts(R):
    if isinstance(R, dict):
        elements = R['elements']
        add = R['add']
        mul = R['mul']
        zero = R['zero']
    else:
        elements = R.elements
        add = R.add
        mul = R.mul
        zero = R.zero
        
    if isinstance(add, dict):
        add_func = lambda a, b: add[(a, b)]
    else:
        add_func = add
        
    if isinstance(mul, dict):
        mul_func = lambda a, b: mul[(a, b)]
    else:
        mul_func = mul
        
    return elements, add_func, mul_func, zero

def is_ring(R):
    try:
        elements, add, mul, zero = get_ring_parts(R)
        
        if zero not in elements: return False
        
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a: return False
            has_inv = False
            for b in elements:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                if add(a, b) != add(b, a): return False
            if not has_inv: return False
            
        for a in elements:
            for b in elements:
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        return True
    except Exception:
        return False

def is_ring_hom(f, R, S):
    try:
        R_elems, R_add, R_mul, R_zero = get_ring_parts(R)
        S_elems, S_add, S_mul, S_zero = get_ring_parts(S)
        
        if isinstance(f, dict):
            f_func = lambda x: f[x]
        else:
            f_func = f
            
        for a in R_elems:
            fa = f_func(a)
            if fa not in S_elems: return False
            for b in R_elems:
                fb = f_func(b)
                if f_func(R_add(a, b)) != S_add(fa, fb): return False
                if f_func(R_mul(a, b)) != S_mul(fa, fb): return False
        return True
    except Exception:
        return False

def is_ideal(I, R):
    try:
        R_elems, R_add, R_mul, R_zero = get_ring_parts(R)
        
        if not all(x in R_elems for x in I): return False
        if R_zero not in I: return False
        
        for a in I:
            for b in I:
                minus_b = None
                for x in R_elems:
                    if R_add(b, x) == R_zero:
                        minus_b = x
                        break
                if minus_b is None: return False
                if R_add(a, minus_b) not in I: return False
                
        is_left = True
        for r in R_elems:
            for x in I:
                if R_mul(r, x) not in I:
                    is_left = False
                    break
            if not is_left: break
            
        is_right = True
        for r in R_elems:
            for x in I:
                if R_mul(x, r) not in I:
                    is_right = False
                    break
            if not is_right: break
            
        return is_left or is_right
    except Exception:
        return False

def is_two_sided_ideal(I, R):
    try:
        R_elems, R_add, R_mul, R_zero = get_ring_parts(R)
        
        if not all(x in R_elems for x in I): return False
        if R_zero not in I: return False
        
        for a in I:
            for b in I:
                minus_b = None
                for x in R_elems:
                    if R_add(b, x) == R_zero:
                        minus_b = x
                        break
                if minus_b is None: return False
                if R_add(a, minus_b) not in I: return False
                
        for r in R_elems:
            for x in I:
                if R_mul(r, x) not in I: return False
                if R_mul(x, r) not in I: return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    R = witness.get('R')
    S = witness.get('S')
    f = witness.get('f')
    I = witness.get('I')
    
    # H1: R and S are rings
    try:
        h1 = is_ring(R) and is_ring(S)
    except Exception:
        h1 = False
        
    # H2: f is a ring homomorphism
    try:
        h2 = is_ring_hom(f, R, S)
    except Exception:
        h2 = False
        
    # H3: I is an ideal of R such that I <= ker(f)
    try:
        R_elems, R_add, R_mul, R_zero = get_ring_parts(R)
        S_elems, S_add, S_mul, S_zero = get_ring_parts(S)
        if isinstance(f, dict):
            f_func = lambda x: f[x]
        else:
            f_func = f
            
        is_id = is_ideal(I, R)
        in_ker = all(f_func(x) == S_zero for x in I)
        h3 = is_id and in_ker
    except Exception:
        h3 = False
        
    # Negated Conclusion: R/I is not a ring (I is not a two-sided ideal), so no such ring homomorphism exists
    try:
        neg_q = not is_two_sided_ideal(I, R)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a ring homomorphism",
    "H_3: I is an ideal of R such that I is a subset of ker(f)",
    "¬Q: R/I is not a ring (I is not a two-sided ideal), so no such ring homomorphism exists"
]

N_HYP = 3
NEG_Q_INDEX = 3
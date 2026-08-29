import sympy
from sympy import *
import math
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(R):
    try:
        if isinstance(R, dict) and 'elements' in R: return R['elements']
        if hasattr(R, 'elements'):
            el = R.elements
            if callable(el): return el()
            return el
        if isinstance(R, (list, tuple, set)): return list(R)
    except Exception:
        pass
    return None

def get_add(R):
    try:
        if isinstance(R, dict) and 'add' in R: return R['add']
        if hasattr(R, 'add'): return R.add
    except Exception:
        pass
    return lambda a, b: a + b

def get_mul(R):
    try:
        if isinstance(R, dict) and 'mul' in R: return R['mul']
        if hasattr(R, 'mul'): return R.mul
    except Exception:
        pass
    return lambda a, b: a * b

def get_zero(R):
    try:
        if isinstance(R, dict) and 'zero' in R: return R['zero']
        if hasattr(R, 'zero'): return R.zero
        elements = get_elements(R)
        add = get_add(R)
        if elements:
            for z in elements:
                if all(add(a, z) == a and add(z, a) == a for a in elements):
                    return z
    except Exception:
        pass
    return 0

def is_boolean_ring(R):
    elements = get_elements(R)
    if elements is None:
        return False
    
    add = get_add(R)
    mul = get_mul(R)
    zero = get_zero(R)
    
    if zero not in elements:
        return False
        
    # Check abelian group under addition
    for a in elements:
        if add(a, zero) != a or add(zero, a) != a: return False
        has_inv = False
        for b in elements:
            ab = add(a, b)
            if ab not in elements: return False
            if ab == zero: has_inv = True
            if ab != add(b, a): return False
        if not has_inv: return False
        
    # Check associativity of addition
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                
    # Check closure and associativity of multiplication
    for a in elements:
        for b in elements:
            ab = mul(a, b)
            if ab not in elements: return False
            for c in elements:
                if mul(ab, c) != mul(a, mul(b, c)): return False
                
    # Check distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                
    # Check Boolean property (x^2 = x)
    for a in elements:
        if mul(a, a) != a: return False
        
    return True

def unpack_witness(witness):
    R = None
    x = None
    n = None
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            x = witness.get('x')
            n = witness.get('n')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                R, x = witness
            elif len(witness) >= 3:
                R, x, n = witness[:3]
        else:
            if hasattr(witness, 'R'): R = witness.R
            if hasattr(witness, 'x'): x = witness.x
            if hasattr(witness, 'n'): n = witness.n
    except Exception:
        pass
    return R, x, n

def conditions(witness) -> list[bool]:
    R, x, n = unpack_witness(witness)
    
    # H_1: R is a Boolean ring
    try:
        h1 = is_boolean_ring(R)
    except Exception:
        h1 = False
        
    # H_2: There exists a positive integer n such that x^n = 0
    try:
        elements = get_elements(R)
        if elements is not None and x not in elements:
            h2 = False
        else:
            mul = get_mul(R)
            zero = get_zero(R)
            
            if n is not None:
                if isinstance(n, int) and n > 0 and n <= 1000:
                    res = x
                    for _ in range(n - 1):
                        res = mul(res, x)
                    h2 = bool(res == zero)
                else:
                    h2 = False
            else:
                res = x
                h2 = False
                if res == zero:
                    h2 = True
                else:
                    for _ in range(2, 20):
                        res = mul(res, x)
                        if res == zero:
                            h2 = True
                            break
    except Exception:
        h2 = False
        
    # ¬Q: x != 0
    try:
        zero = get_zero(R)
        neg_q = bool(x != zero)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: There exists a positive integer n such that x^n = 0",
    "¬Q: x != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2
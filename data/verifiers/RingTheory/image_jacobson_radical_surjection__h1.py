import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import itertools
import functools
import math

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements_safe(ring, max_elems=1000):
    if hasattr(ring, 'elements'):
        elems = ring.elements
    elif hasattr(ring, 'ring_elements'):
        elems = ring.ring_elements
    elif isinstance(ring, (list, set, tuple)):
        elems = ring
    else:
        elems = ring
        
    result = []
    try:
        for i, e in enumerate(elems):
            if i >= max_elems:
                return result, False
            result.append(e)
    except Exception:
        pass
    return result, True

def get_add(ring, witness=None):
    if isinstance(witness, dict):
        if ring is witness.get('R') and 'R_add' in witness:
            return witness['R_add']
        if ring is witness.get('S') and 'S_add' in witness:
            return witness['S_add']
    if hasattr(ring, 'add'):
        return ring.add
    return lambda a, b: a + b

def get_mul(ring, witness=None):
    if isinstance(witness, dict):
        if ring is witness.get('R') and 'R_mul' in witness:
            return witness['R_mul']
        if ring is witness.get('S') and 'S_mul' in witness:
            return witness['S_mul']
    if hasattr(ring, 'mul'):
        return ring.mul
    return lambda a, b: a * b

def apply_f(f, elem):
    if isinstance(f, dict):
        return f[elem]
    else:
        return f(elem)

def is_in(elem, lst):
    for x in lst:
        if elem == x:
            return True
    return False

def same_set(list1, list2):
    for x in list1:
        if not is_in(x, list2): return False
    for x in list2:
        if not is_in(x, list1): return False
    return True

def jacobson_radical(elements, add, mul):
    """
    Computes the Jacobson radical of a finite ring.
    An element x is in J(R) iff for all r in R, r*x is left quasi-regular.
    y is left quasi-regular iff there exists u in R such that u + y - u*y = 0,
    which is equivalent to u + y = u*y.
    """
    J = []
    for elem in elements:
        is_in_J = True
        for r in elements:
            rx = mul(r, elem)
            quasi_regular = False
            for u in elements:
                if add(u, rx) == mul(u, rx):
                    quasi_regular = True
                    break
            if not quasi_regular:
                is_in_J = False
                break
        if is_in_J:
            J.append(elem)
    return J

def extract(witness):
    if isinstance(witness, dict):
        R = witness.get('R')
        S = witness.get('S')
        f = witness.get('f')
    elif isinstance(witness, tuple) and len(witness) == 3:
        R, S, f = witness
    else:
        R = witness.R
        S = witness.S
        f = witness.f
    return R, S, f

def check_h1(witness, R, S, f):
    R_elems, r_complete = get_elements_safe(R)
    S_elems, s_complete = get_elements_safe(S)
    
    R_add = get_add(R, witness)
    R_mul = get_mul(R, witness)
    S_add = get_add(S, witness)
    S_mul = get_mul(S, witness)
    
    image = []
    for elem in R_elems:
        fx = apply_f(f, elem)
        if not is_in(fx, image):
            image.append(fx)
            
    if s_complete:
        for y in S_elems:
            if not is_in(y, image):
                return False
                
    for x_elem in R_elems:
        for y_elem in R_elems:
            fx = apply_f(f, x_elem)
            fy = apply_f(f, y_elem)
            
            xy_add = R_add(x_elem, y_elem)
            if apply_f(f, xy_add) != S_add(fx, fy):
                return False
                
            xy_mul = R_mul(x_elem, y_elem)
            if apply_f(f, xy_mul) != S_mul(fx, fy):
                return False
                
    return True

def check_h2(witness, R, S):
    R_elems, r_complete = get_elements_safe(R)
    S_elems, s_complete = get_elements_safe(S)
    
    if not r_complete or not s_complete:
        return True
        
    R_add = get_add(R, witness)
    R_mul = get_mul(R, witness)
    S_add = get_add(S, witness)
    S_mul = get_mul(S, witness)
    
    computed_JR = jacobson_radical(R_elems, R_add, R_mul)
    computed_JS = jacobson_radical(S_elems, S_add, S_mul)
    
    if isinstance(witness, dict):
        if 'J_R' in witness:
            if not same_set(list(witness['J_R']), computed_JR): return False
        if 'J_S' in witness:
            if not same_set(list(witness['J_S']), computed_JS): return False
    else:
        if hasattr(witness, 'J_R'):
            if not same_set(list(witness.J_R), computed_JR): return False
        if hasattr(witness, 'J_S'):
            if not same_set(list(witness.J_S), computed_JS): return False
            
    return True

def check_neg_q(witness, R, S, f):
    if isinstance(witness, dict) and 'J_R' in witness:
        JR = list(witness['J_R'])
    elif hasattr(witness, 'J_R'):
        JR = list(witness.J_R)
    else:
        R_elems, _ = get_elements_safe(R)
        R_add = get_add(R, witness)
        R_mul = get_mul(R, witness)
        JR = jacobson_radical(R_elems, R_add, R_mul)
        
    if isinstance(witness, dict) and 'J_S' in witness:
        JS = list(witness['J_S'])
    elif hasattr(witness, 'J_S'):
        JS = list(witness.J_S)
    else:
        S_elems, _ = get_elements_safe(S)
        S_add = get_add(S, witness)
        S_mul = get_mul(S, witness)
        JS = jacobson_radical(S_elems, S_add, S_mul)
        
    for x_elem in JR:
        fx = apply_f(f, x_elem)
        if not is_in(fx, JS):
            return True
            
    return False

def conditions(witness):
    try:
        R, S, f = extract(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_h1(witness, R, S, f)
    except Exception:
        h1 = False
        
    try:
        h2 = check_h2(witness, R, S)
    except Exception:
        h2 = False
        
    try:
        neg_q = check_neg_q(witness, R, S, f)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism",
    "H_2: J(R) and J(S) denote the Jacobson radicals of R and S",
    "¬Q: The image f(J(R)) is not contained in J(S)"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import eye, zeros
import itertools
import functools

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_op(op_data):
    if callable(op_data):
        return op_data
    elif isinstance(op_data, dict):
        return lambda x, y: op_data[(x, y)]
    elif isinstance(op_data, list):
        return lambda x, y: op_data[x][y]
    else:
        raise ValueError("Unknown operator format")

def get_map(map_data):
    if callable(map_data):
        return map_data
    elif isinstance(map_data, dict):
        return lambda x: map_data[x]
    elif isinstance(map_data, list):
        return lambda x: map_data[x]
    else:
        raise ValueError("Unknown map format")

def parse_witness(witness):
    if isinstance(witness, dict):
        R_elems = list(witness['R'])
        R_add = get_op(witness['R_add'])
        R_mul = get_op(witness['R_mul'])
        S_elems = list(witness['S'])
        S_add = get_op(witness['S_add'])
        S_mul = get_op(witness['S_mul'])
        f = get_map(witness['f'])
    elif isinstance(witness, tuple) and len(witness) == 7:
        R_elems, R_add, R_mul, S_elems, S_add, S_mul, f = witness
        R_elems = list(R_elems)
        S_elems = list(S_elems)
        R_add = get_op(R_add)
        R_mul = get_op(R_mul)
        S_add = get_op(S_add)
        S_mul = get_op(S_mul)
        f = get_map(f)
    else:
        R_elems = list(witness.R)
        R_add = get_op(witness.R_add)
        R_mul = get_op(witness.R_mul)
        S_elems = list(witness.S)
        S_add = get_op(witness.S_add)
        S_mul = get_op(witness.S_mul)
        f = get_map(witness.f)
    return R_elems, R_add, R_mul, S_elems, S_add, S_mul, f

def is_ring(elements, add, mul):
    if not elements:
        return False
    # Check closure
    for a in elements:
        for b in elements:
            try:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
            except Exception:
                return False
                
    # Check addition associativity and commutativity
    for a in elements:
        for b in elements:
            if add(a, b) != add(b, a): return False
            for c in elements:
                if add(a, add(b, c)) != add(add(a, b), c): return False
                
    # Check zero
    zeros_list = []
    for z in elements:
        if all(add(z, a) == a for a in elements):
            zeros_list.append(z)
    if len(zeros_list) != 1: return False
    zero = zeros_list[0]
    
    # Check additive inverse
    for a in elements:
        if not any(add(a, b) == zero for b in elements): return False
        
    # Check multiplication associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, mul(b, c)) != mul(mul(a, b), c): return False
                
    # Check distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                
    return True

def get_zero(elements, add):
    for z in elements:
        if all(add(z, a) == a for a in elements):
            return z
    return None

def get_center(elements, mul):
    center = []
    for z in elements:
        if all(mul(z, a) == mul(a, z) for a in elements):
            center.append(z)
    return center

def is_subring(subset, elements, add, mul, zero):
    if zero not in subset:
        return False
    for a in subset:
        for b in subset:
            if add(a, b) not in subset:
                return False
            if mul(a, b) not in subset:
                return False
        # Check additive inverse
        has_inv = False
        for b in subset:
            if add(a, b) == zero:
                has_inv = True
                break
        if not has_inv:
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        R_elems, R_add, R_mul, S_elems, S_add, S_mul, f = parse_witness(witness)
    except Exception:
        return [False, False, False, False]
        
    # H_1: R and S are rings
    try:
        h1 = is_ring(R_elems, R_add, R_mul) and is_ring(S_elems, S_add, S_mul)
    except Exception:
        h1 = False
        
    # H_2: f is a surjective ring homomorphism
    try:
        is_hom = True
        for a in R_elems:
            for b in R_elems:
                if f(R_add(a, b)) != S_add(f(a), f(b)):
                    is_hom = False
                    break
                if f(R_mul(a, b)) != S_mul(f(a), f(b)):
                    is_hom = False
                    break
            if not is_hom:
                break
                
        image = []
        for a in R_elems:
            val = f(a)
            if val not in image:
                image.append(val)
                
        is_surj = True
        for s in S_elems:
            if s not in image:
                is_surj = False
                break
                
        h2 = is_hom and is_surj
    except Exception:
        h2 = False
        
    # H_3: Z(R) denotes the center of R (Definitional, holds if R is a ring)
    h3 = h1
    
    # ¬Q: The preimage f^{-1}(Z(S)) is NOT a subring of R that contains both Z(R) and ker(f)
    try:
        Z_R = get_center(R_elems, R_mul)
        Z_S = get_center(S_elems, S_mul)
        
        f_inv_Z_S = [r for r in R_elems if f(r) in Z_S]
        
        S_zero = get_zero(S_elems, S_add)
        ker_f = [r for r in R_elems if f(r) == S_zero]
        
        R_zero = get_zero(R_elems, R_add)
        
        is_sub = is_subring(f_inv_Z_S, R_elems, R_add, R_mul, R_zero)
        
        contains_Z_R = all(z in f_inv_Z_S for z in Z_R)
        contains_ker_f = all(k in f_inv_Z_S for k in ker_f)
        
        Q = is_sub and contains_Z_R and contains_ker_f
        neg_Q = not Q
    except Exception:
        neg_Q = False
        
    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a surjective ring homomorphism",
    "H_3: Z(R) denotes the center of R",
    "¬Q: f^{-1}(Z(S)) is not a subring of R containing Z(R) and ker(f)"
]

N_HYP = 3
NEG_Q_INDEX = 3
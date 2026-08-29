import sympy
import itertools
import functools
import math

def get_ring_data(ring):
    if hasattr(ring, 'elements') and hasattr(ring, 'add') and hasattr(ring, 'mul'):
        return list(ring.elements), ring.add, ring.mul, ring.zero, ring.one
    if isinstance(ring, dict):
        return list(ring['elements']), ring['add'], ring['mul'], ring['zero'], ring['one']
    raise ValueError("Unknown ring format")

def extract_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 3:
        return witness[0], witness[1], witness[2]
    if isinstance(witness, dict):
        return witness['R'], witness['S'], witness['f']
    return witness.R, witness.S, witness.f

def check_ring(elements, add, mul, zero, one):
    if zero not in elements or one not in elements:
        return False
    for a in elements:
        if add(a, zero) != a or add(zero, a) != a:
            return False
        if mul(a, one) != a or mul(one, a) != a:
            return False
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv:
            return False
    return True

def check_homomorphism(R_elements, R_add, R_mul, R_one, S_add, S_mul, S_one, f):
    if f(R_one) != S_one:
        return False
    for a in R_elements:
        for b in R_elements:
            if f(R_add(a, b)) != S_add(f(a), f(b)):
                return False
            if f(R_mul(a, b)) != S_mul(f(a), f(b)):
                return False
    return True

def check_Q(R_elements, R_add, R_mul, R_zero, R_one, S_elements, S_add, S_mul, S_zero, S_one, f):
    R_units = []
    for u in R_elements:
        for v in R_elements:
            if R_mul(u, v) == R_one and R_mul(v, u) == R_one:
                R_units.append(u)
                break
                
    S_units = []
    for s in S_elements:
        for t in S_elements:
            if S_mul(s, t) == S_one and S_mul(t, s) == S_one:
                S_units.append(s)
                break
                
    ker_f_times = []
    for u in R_units:
        fu = f(u)
        if fu not in S_units:
            return False
        if fu == S_one:
            ker_f_times.append(u)
            
    neg_one = None
    for x in R_elements:
        if R_add(R_one, x) == R_zero:
            neg_one = x
            break
            
    H = []
    for u in R_units:
        u_minus_1 = R_add(u, neg_one)
        if f(u_minus_1) == S_zero:
            H.append(u)
            
    if R_one not in H:
        return False
    for a in H:
        for b in H:
            if R_mul(a, b) not in H:
                return False
        inv_a = None
        for v in R_elements:
            if R_mul(a, v) == R_one and R_mul(v, a) == R_one:
                inv_a = v
                break
        if inv_a not in H:
            return False
            
    for x in ker_f_times:
        if x not in H:
            return False
    for x in H:
        if x not in ker_f_times:
            return False
            
    return True

def conditions(witness):
    try:
        R, S, f_map = extract_witness(witness)
        R_elements, R_add, R_mul, R_zero, R_one = get_ring_data(R)
        S_elements, S_add, S_mul, S_zero, S_one = get_ring_data(S)
        
        if isinstance(f_map, dict):
            f = lambda x: f_map[x]
        elif isinstance(f_map, list):
            f = lambda x: f_map[x]
        else:
            f = f_map
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_ring(R_elements, R_add, R_mul, R_zero, R_one) and \
             check_ring(S_elements, S_add, S_mul, S_zero, S_one)
    except Exception:
        h1 = False
        
    try:
        h2 = check_homomorphism(R_elements, R_add, R_mul, R_one, S_add, S_mul, S_one, f)
    except Exception:
        h2 = False
        
    try:
        q = check_Q(R_elements, R_add, R_mul, R_zero, R_one, S_elements, S_add, S_mul, S_zero, S_one, f)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f is a ring homomorphism such that f(1_R) = 1_S",
    "¬Q: The kernel of f^x is not the subgroup of R^x consisting of all units u such that u - 1 in ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2
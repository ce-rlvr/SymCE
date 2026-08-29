import sympy as sp
from sympy import eye, zeros, Matrix

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mat_or_scalar(c):
    if hasattr(c, 'is_zero_matrix'):
        if c.is_zero_matrix is not None:
            return c.is_zero_matrix
        return all(sp.simplify(val) == 0 for val in c)
    else:
        return sp.simplify(c) == 0

def is_identity_poly(p):
    if not p: return False
    try:
        I = p[0]**0
    except Exception:
        I = 1
    if not is_zero_mat_or_scalar(p[0] - I):
        return False
    for c in p[1:]:
        if not is_zero_mat_or_scalar(c):
            return False
    return True

def check_H1(witness):
    if isinstance(witness, dict):
        f_coeffs = witness.get('f', [])
    elif isinstance(witness, list):
        f_coeffs = witness
    else:
        return False
        
    if not isinstance(f_coeffs, list) or len(f_coeffs) == 0:
        return False
        
    first = f_coeffs[0]
    if hasattr(first, 'shape'):
        shape = first.shape
        if len(shape) != 2 or shape[0] != shape[1]:
            return False
        for c in f_coeffs[1:]:
            if not hasattr(c, 'shape') or c.shape != shape:
                return False
    else:
        for c in f_coeffs[1:]:
            if hasattr(c, 'shape'):
                return False
    return True

def check_f_is_unit(f_coeffs, g_coeffs=None):
    if g_coeffs is not None:
        def poly_mul(p1, p2):
            if not p1 or not p2: return []
            zero = p1[0] * 0
            res = [zero] * (len(p1) + len(p2) - 1)
            for i in range(len(p1)):
                for j in range(len(p2)):
                    res[i+j] = res[i+j] + p1[i] * p2[j]
            return res
        
        fg = poly_mul(f_coeffs, g_coeffs)
        gf = poly_mul(g_coeffs, f_coeffs)
        
        if is_identity_poly(fg) and is_identity_poly(gf):
            return True

    x = sp.Symbol('__x_var__')
    F = f_coeffs[0] * 1
    for i in range(1, len(f_coeffs)):
        F = F + f_coeffs[i] * (x**i)
    
    if hasattr(F, 'det'):
        d = F.det()
        d = sp.expand(d)
        if d == 0:
            return False
        if not d.has(x):
            return True
        return False
    else:
        if len(f_coeffs) == 1:
            return sp.simplify(f_coeffs[0]) != 0
        return False

def check_a0_is_unit(f_coeffs):
    a0 = f_coeffs[0]
    if hasattr(a0, 'det'):
        d = a0.det()
        d = sp.expand(d)
        if d == 0:
            return False
        return True
    else:
        return sp.simplify(a0) != 0

def check_all_nilpotent(f_coeffs):
    if len(f_coeffs) <= 1:
        return True
    
    for a in f_coeffs[1:]:
        if hasattr(a, 'shape'):
            n = a.shape[0]
            an = a**n
            if not is_zero_mat_or_scalar(an):
                return False
        else:
            if sp.simplify(a) != 0:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        h1 = check_H1(witness)
    except Exception:
        h1 = False
        
    if not h1:
        return [False, False]
        
    try:
        if isinstance(witness, dict):
            f_coeffs = witness.get('f', [])
            g_coeffs = witness.get('g', None)
        else:
            f_coeffs = witness
            g_coeffs = None
            
        f_is_unit = check_f_is_unit(f_coeffs, g_coeffs)
        a0_is_unit = check_a0_is_unit(f_coeffs)
        all_nilp = check_all_nilpotent(f_coeffs)
        
        Q = (f_is_unit == (a0_is_unit and all_nilp))
        neg_Q = not Q
    except Exception:
        neg_Q = False
        
    return [h1, neg_Q]

CONDITION_LABELS = [
    "H_1: f is a polynomial over R",
    "not Q: The equivalence for f being a unit fails"
]

N_HYP = 1
NEG_Q_INDEX = 1
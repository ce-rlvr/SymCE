import sympy
from sympy import eye, zeros
import itertools
import functools
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def find_zero(elements, add):
    elements = list(elements)
    for z in elements:
        is_z = True
        for a in elements:
            if add(z, a) != a or add(a, z) != a:
                is_z = False
                break
        if is_z:
            return z
    return None

def is_ring(elements, add, mul):
    elements = list(elements)
    z = find_zero(elements, add)
    if z is None: return False
    for a in elements:
        has_inv = False
        for b in elements:
            if add(a, b) == z and add(b, a) == z:
                has_inv = True
                break
        if not has_inv:
            return False
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

def get_ops(witness, prefix):
    if hasattr(witness, f"{prefix}_add"):
        add = getattr(witness, f"{prefix}_add")
    else:
        add = lambda a, b: a + b
    if hasattr(witness, f"{prefix}_mul"):
        mul = getattr(witness, f"{prefix}_mul")
    else:
        mul = lambda a, b: a * b
    return add, mul

def is_poly_zero(poly, S_zero):
    if hasattr(poly, 'is_zero'):
        val = poly.is_zero
        return val() if callable(val) else val
    if isinstance(poly, (list, tuple)):
        return all(c == S_zero for c in poly)
    else:
        return poly == S_zero

def get_polys(R, max_degree):
    polys = []
    R_list = list(R)
    for deg in range(max_degree + 1):
        for p in itertools.product(R_list, repeat=deg + 1):
            polys.append(p)
    return polys

def conditions(witness):
    try:
        R_add, R_mul = get_ops(witness, "R")
        S_add, S_mul = get_ops(witness, "S")
        h1 = is_ring(witness.R, R_add, R_mul) and is_ring(witness.S, S_add, S_mul)
    except Exception:
        h1 = False

    try:
        f = witness.f
        R_add, R_mul = get_ops(witness, "R")
        S_add, S_mul = get_ops(witness, "S")
        h2 = True
        R_list = list(witness.R)
        S_list = list(witness.S)
        for a in R_list:
            if f(a) not in S_list:
                h2 = False
                break
            for b in R_list:
                if f(R_add(a, b)) != S_add(f(a), f(b)):
                    h2 = False
                    break
                if f(R_mul(a, b)) != S_mul(f(a), f(b)):
                    h2 = False
                    break
        
        def find_one(elements, mul):
            for e in elements:
                is_one = True
                for a in elements:
                    if mul(e, a) != a or mul(a, e) != a:
                        is_one = False
                        break
                if is_one:
                    return e
            return None
        
        R_one = find_one(R_list, R_mul)
        S_one = find_one(S_list, S_mul)
        if R_one is not None and S_one is not None:
            if f(R_one) != S_one:
                h2 = False

    except Exception:
        h2 = False

    try:
        R_add, _ = get_ops(witness, "R")
        S_add, _ = get_ops(witness, "S")
        R_zero = find_zero(witness.R, R_add)
        S_zero = find_zero(witness.S, S_add)
        
        f = witness.f
        F = witness.F
        
        neg_q = False
        for P in get_polys(witness.R, 2):
            all_in_ker = all(f(c) == S_zero for c in P)
            F_P = F(P)
            is_F_P_zero = is_poly_zero(F_P, S_zero)
            if is_F_P_zero != all_in_ker:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a ring homomorphism from R to S",
    "neg_Q: kernel of F is not the ideal of polynomials over R with coefficients in ker f"
]

N_HYP = 2
NEG_Q_INDEX = 2
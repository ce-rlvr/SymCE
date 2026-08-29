import sympy
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: I is a primary ideal iff every zero divisor in R/I is nilpotent is FALSE"
]
N_HYP = 1
NEG_Q_INDEX = 1

def in_list(lst, elem):
    for x in lst:
        try:
            if bool(x == elem):
                return True
        except Exception:
            pass
    return False

def get_neg(y, neg_list):
    for k, v in neg_list:
        try:
            if bool(k == y):
                return v
        except Exception:
            pass
    return None

def parse_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) == 2:
            R, I = witness
            add = lambda a, b: a + b
            mul = lambda a, b: a * b
            return R, I, add, mul
        elif len(witness) >= 4:
            R = witness[0]
            I = witness[1]
            add = witness[2]
            mul = witness[3]
            return R, I, add, mul
    elif hasattr(witness, 'R') and hasattr(witness, 'I'):
        R = witness.R
        I = witness.I
        add = getattr(witness, 'add', lambda a, b: a + b)
        mul = getattr(witness, 'mul', lambda a, b: a * b)
        return R, I, add, mul
    return None, None, None, None

def generate_ideal(R, S, add, mul, zero, neg_list):
    ideal = []
    for x in S:
        if not in_list(ideal, x):
            ideal.append(x)
    added = True
    while added:
        added = False
        new_elements = []
        for x in ideal:
            for r in R:
                rx = mul(r, x)
                if not in_list(ideal, rx) and not in_list(new_elements, rx):
                    new_elements.append(rx)
                xr = mul(x, r)
                if not in_list(ideal, xr) and not in_list(new_elements, xr):
                    new_elements.append(xr)
            for y in ideal:
                xy = add(x, y)
                if not in_list(ideal, xy) and not in_list(new_elements, xy):
                    new_elements.append(xy)
                
                neg_y = get_neg(y, neg_list)
                if neg_y is not None:
                    x_y = add(x, neg_y)
                    if not in_list(ideal, x_y) and not in_list(new_elements, x_y):
                        new_elements.append(x_y)
        if new_elements:
            ideal.extend(new_elements)
            added = True
    return ideal

def multiply_ideals(R, A, B, add, mul, zero, neg_list):
    products = []
    for a in A:
        for b in B:
            ab = mul(a, b)
            if not in_list(products, ab):
                products.append(ab)
    return generate_ideal(R, products, add, mul, zero, neg_list)

def is_proper_ideal(R, I, add, mul, zero, neg_list):
    if not I: return False
    if len(I) == len(R): return False
    for x in I:
        if not in_list(R, x): return False
    
    if not in_list(I, zero): return False
    
    for x in I:
        for y in I:
            neg_y = get_neg(y, neg_list)
            if neg_y is None: return False
            if not in_list(I, add(x, neg_y)): return False
            
    for r in R:
        for x in I:
            if not in_list(I, mul(r, x)): return False
            if not in_list(I, mul(x, r)): return False
            
    return True

def is_primary_ideal(R, I, add, mul, zero, neg_list):
    principal_ideals = []
    for x in R:
        principal_ideals.append(generate_ideal(R, [x], add, mul, zero, neg_list))
        
    for i, a in enumerate(R):
        A = principal_ideals[i]
        for j, b in enumerate(R):
            B = principal_ideals[j]
            
            ab_in_I = True
            for x in A:
                for y in B:
                    if not in_list(I, mul(x, y)):
                        ab_in_I = False
                        break
                if not ab_in_I:
                    break
            
            if ab_in_I:
                if in_list(I, a):
                    continue
                
                B_pow = B
                B_pow_in_I = False
                for _ in range(len(R) + 1):
                    subset = True
                    for x in B_pow:
                        if not in_list(I, x):
                            subset = False
                            break
                    if subset:
                        B_pow_in_I = True
                        break
                    B_pow = multiply_ideals(R, B_pow, B, add, mul, zero, neg_list)
                
                if not B_pow_in_I:
                    return False
    return True

def every_zd_is_nilpotent(R, I, add, mul, zero):
    for x in R:
        is_zd = False
        for y in R:
            if not in_list(I, y):
                if in_list(I, mul(x, y)) or in_list(I, mul(y, x)):
                    is_zd = True
                    break
        if is_zd:
            x_nil = False
            p = x
            for _ in range(len(R) + 1):
                if in_list(I, p):
                    x_nil = True
                    break
                p = mul(p, x)
            if not x_nil:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        R, I, add, mul = parse_witness(witness)
        if R is None:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        zero = None
        for z in R:
            is_zero = True
            for x in R:
                if not bool(add(z, x) == x):
                    is_zero = False
                    break
            if is_zero:
                zero = z
                break
        if zero is None:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        neg_list = []
        for y in R:
            for z in R:
                if bool(add(y, z) == zero):
                    neg_list.append((y, z))
                    break
    except Exception:
        return [False, False]

    try:
        h1 = is_proper_ideal(R, I, add, mul, zero, neg_list)
    except Exception:
        h1 = False

    try:
        primary = is_primary_ideal(R, I, add, mul, zero, neg_list)
        zd_nil = every_zd_is_nilpotent(R, I, add, mul, zero)
        neg_q = bool(primary != zd_nil)
    except Exception:
        neg_q = False

    return [h1, neg_q]
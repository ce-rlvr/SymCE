import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def apply_op(op, x, y):
    if callable(op):
        return op(x, y)
    if isinstance(op, dict):
        return op[(x, y)]
    return op[x][y]

def apply_f(f, x):
    if callable(f):
        return f(x)
    return f[x]

def is_ring(elems, add, mul, zero, one):
    if not elems: return False
    if zero not in elems or one not in elems: return False
    for x in elems:
        if apply_op(add, x, zero) != x: return False
        if apply_op(add, zero, x) != x: return False
        if apply_op(mul, x, one) != x: return False
        if apply_op(mul, one, x) != x: return False
        
        has_inv = False
        for y in elems:
            if apply_op(add, x, y) == zero and apply_op(add, y, x) == zero:
                has_inv = True
                break
        if not has_inv: return False

    for x in elems:
        for y in elems:
            xy_add = apply_op(add, x, y)
            xy_mul = apply_op(mul, x, y)
            if xy_add not in elems: return False
            if xy_mul not in elems: return False
            if xy_add != apply_op(add, y, x): return False
            for z in elems:
                if apply_op(add, xy_add, z) != apply_op(add, x, apply_op(add, y, z)): return False
                if apply_op(mul, xy_mul, z) != apply_op(mul, x, apply_op(mul, y, z)): return False
                if apply_op(mul, x, apply_op(add, y, z)) != apply_op(add, apply_op(mul, x, y), apply_op(mul, x, z)): return False
                if apply_op(mul, apply_op(add, x, y), z) != apply_op(add, apply_op(mul, x, z), apply_op(mul, y, z)): return False
    return True

def is_boolean_ring(elems, add, mul, zero, one):
    if not is_ring(elems, add, mul, zero, one):
        return False
    for x in elems:
        if apply_op(mul, x, x) != x:
            return False
    return True

def extract(witness):
    keys = ['R_elements', 'R_add', 'R_mul', 'R_zero', 'R_one',
            'S_elements', 'S_add', 'S_mul', 'S_zero', 'S_one', 'f']
    if isinstance(witness, dict):
        return tuple(witness[k] for k in keys)
    else:
        return tuple(getattr(witness, k) for k in keys)

def conditions(witness):
    try:
        R_elems, R_add, R_mul, R_zero, R_one, \
        S_elems, S_add, S_mul, S_zero, S_one, f = extract(witness)
    except Exception:
        return [False, False, False]

    # H1: R is a Boolean ring
    try:
        h1 = is_boolean_ring(R_elems, R_add, R_mul, R_zero, R_one)
    except Exception:
        h1 = False

    # H2: f is a ring homomorphism from R to S
    try:
        S_is_ring = is_ring(S_elems, S_add, S_mul, S_zero, S_one)
        if not S_is_ring:
            h2 = False
        else:
            h2 = True
            for x in R_elems:
                fx = apply_f(f, x)
                if fx not in S_elems:
                    h2 = False
                    break
                for y in R_elems:
                    fy = apply_f(f, y)
                    f_add = apply_f(f, apply_op(R_add, x, y))
                    f_mul = apply_f(f, apply_op(R_mul, x, y))
                    if f_add != apply_op(S_add, fx, fy):
                        h2 = False
                        break
                    if f_mul != apply_op(S_mul, fx, fy):
                        h2 = False
                        break
                if not h2: break
    except Exception:
        h2 = False

    # Negated Conclusion: The image of R under f is NOT a Boolean subring of S
    try:
        img = []
        for x in R_elems:
            fx = apply_f(f, x)
            if fx not in img:
                img.append(fx)
        
        is_subring = True
        if S_zero not in img: is_subring = False
        if S_one not in img: is_subring = False
        
        if is_subring:
            for x in img:
                has_inv = False
                for y in img:
                    if apply_op(S_add, x, y) == S_zero and apply_op(S_add, y, x) == S_zero:
                        has_inv = True
                        break
                if not has_inv:
                    is_subring = False
                    break
                
                for y in img:
                    if apply_op(S_add, x, y) not in img:
                        is_subring = False
                        break
                    if apply_op(S_mul, x, y) not in img:
                        is_subring = False
                        break
                if not is_subring: break
        
        is_boolean = True
        if is_subring:
            for x in img:
                if apply_op(S_mul, x, x) != x:
                    is_boolean = False
                    break
                    
        neg_q = not (is_subring and is_boolean)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: f is a ring homomorphism from R to S",
    "¬Q: The image of R under f is not a Boolean subring of S"
]

N_HYP = 2
NEG_Q_INDEX = 2
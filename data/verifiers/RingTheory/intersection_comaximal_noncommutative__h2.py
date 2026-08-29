import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.matrices import *
import math
import itertools
import functools

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def eq(a, b):
    try:
        if a == b:
            return True
    except Exception:
        pass
    try:
        if (a - b) == 0:
            return True
    except Exception:
        pass
    try:
        if (a - b).is_zero:
            return True
    except Exception:
        pass
    return False

def unique_elements(lst):
    res = []
    for x in lst:
        if not any(eq(x, y) for y in res):
            res.append(x)
    return res

def is_subset(sub, sup):
    return all(any(eq(x, y) for y in sup) for x in sub)

def set_eq(A, B):
    return is_subset(A, B) and is_subset(B, A)

def is_ring_with_identity(R):
    if not R: return False
    R = unique_elements(R)
    
    # find zero
    zero = None
    for z in R:
        if all(eq(z + a, a) and eq(a + z, a) for a in R):
            zero = z
            break
    if zero is None: return False
    
    # find one
    one = None
    for e in R:
        if all(eq(e * a, a) and eq(a * e, a) for a in R):
            one = e
            break
    if one is None: return False
    
    # check closures and inverses
    for a in R:
        has_inv = False
        for b in R:
            ab_plus = a + b
            if eq(ab_plus, zero):
                has_inv = True
            if not any(eq(ab_plus, c) for c in R): return False
            
            ab_mul = a * b
            if not any(eq(ab_mul, c) for c in R): return False
        if not has_inv: return False
    return True

def is_ideal(I, R):
    if not I: return False
    if not is_subset(I, R): return False
    # check addition closure
    for a in I:
        for b in I:
            ab_plus = a + b
            if not any(eq(ab_plus, c) for c in I): return False
    # check absorption (two-sided)
    for r in R:
        for x in I:
            rx = r * x
            if not any(eq(rx, c) for c in I): return False
            xr = x * r
            if not any(eq(xr, c) for c in I): return False
    return True

def sum_ideals(I, J):
    res = []
    for x in I:
        for y in J:
            xy = x + y
            if not any(eq(xy, z) for z in res):
                res.append(xy)
    return res

def intersect(I, J):
    res = []
    for x in I:
        if any(eq(x, y) for y in J):
            if not any(eq(x, z) for z in res):
                res.append(x)
    return res

def close_under_addition(S, R):
    if not S: return []
    res = unique_elements(S)
    agenda = list(res)
    max_len = len(R)
    
    while agenda:
        a = agenda.pop()
        new_elements = []
        for b in res:
            c1 = a + b
            if not any(eq(c1, x) for x in res) and not any(eq(c1, x) for x in new_elements):
                new_elements.append(c1)
            c2 = b + a
            if not any(eq(c2, x) for x in res) and not any(eq(c2, x) for x in new_elements):
                new_elements.append(c2)
        
        if new_elements:
            for nx in new_elements:
                res.append(nx)
                agenda.append(nx)
            if len(res) > max_len:
                return res
    return res

def mul_ideals(I, J, R):
    prods = []
    for x in I:
        for y in J:
            xy = x * y
            if not any(eq(xy, z) for z in prods):
                prods.append(xy)
    return close_under_addition(prods, R)

def conditions(witness):
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_ring_with_identity(R) and is_ideal(I, R) and is_ideal(J, R)
    except Exception:
        h1 = False
        
    try:
        h2 = set_eq(sum_ideals(I, J), R)
    except Exception:
        h2 = False
        
    try:
        I_cap_J = intersect(I, J)
        IJ = mul_ideals(I, J, R)
        JI = mul_ideals(J, I, R)
        IJ_plus_JI = sum_ideals(IJ, JI)
        neg_q = not set_eq(I_cap_J, IJ_plus_JI)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity and I, J are ideals",
    "H_2: I + J = R",
    "¬Q: I \\cap J \\neq IJ + JI"
]

N_HYP = 2
NEG_Q_INDEX = 2
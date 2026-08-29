import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import functools
import math

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def contains(lst, item):
    for x in lst:
        if x == item:
            return True
    return False

def is_ring(R):
    if not R: return False
    try:
        R_set = set(R)
        fast_contains = lambda x: x in R_set
    except TypeError:
        fast_contains = lambda x: contains(R, x)
        
    for a in R:
        for b in R:
            if not fast_contains(a + b): return False
            if not fast_contains(a - b): return False
            if not fast_contains(a * b): return False
            
    has_zero = False
    for z in R:
        if all((a + z == a) and (z + a == a) for a in R):
            has_zero = True
            break
    if not has_zero: return False
    
    has_one = False
    for e in R:
        if all((a * e == a) and (e * a == a) for a in R):
            has_one = True
            break
    if not has_one: return False
    
    return True

def is_ideal(R, I):
    if not is_ring(R): return False
    if not I: return False
    
    try:
        R_set = set(R)
        fast_contains_R = lambda x: x in R_set
    except TypeError:
        fast_contains_R = lambda x: contains(R, x)
        
    try:
        I_set = set(I)
        fast_contains_I = lambda x: x in I_set
    except TypeError:
        fast_contains_I = lambda x: contains(I, x)

    for a in I:
        if not fast_contains_R(a): return False
        
    for a in I:
        for b in I:
            if not fast_contains_I(a + b): return False
            if not fast_contains_I(a - b): return False
            
    for a in I:
        for r in R:
            if not fast_contains_I(a * r): return False
            if not fast_contains_I(r * a): return False
            
    return True

def radical(R, J):
    try:
        J_set = set(J)
        fast_contains_J = lambda x: x in J_set
    except TypeError:
        fast_contains_J = lambda x: contains(J, x)
        
    rad = []
    max_steps = len(R)
    for r in R:
        current = r
        is_in_rad = False
        for _ in range(max_steps):
            if fast_contains_J(current):
                is_in_rad = True
                break
            current = current * r
        if is_in_rad:
            rad.append(r)
    return rad

def colon_right(R, J, x):
    try:
        J_set = set(J)
        fast_contains_J = lambda y: y in J_set
    except TypeError:
        fast_contains_J = lambda y: contains(J, y)
        
    return [r for r in R if fast_contains_J(r * x)]

def conditions(witness):
    try:
        R_raw, I_raw, x = witness
        R = list(R_raw)
        I = list(I_raw)
    except Exception:
        return [False, False, False]
        
    def safe_is_ideal():
        try:
            return is_ideal(R, I)
        except Exception:
            return False

    def safe_is_in_R():
        try:
            try:
                R_set = set(R)
                return x in R_set
            except TypeError:
                return contains(R, x)
        except Exception:
            return False

    def safe_neg_q():
        try:
            I_colon_x = colon_right(R, I, x)
            rad_I_colon_x = radical(R, I_colon_x)
            rad_I = radical(R, I)
            rad_I_colon_x_target = colon_right(R, rad_I, x)
            
            try:
                target_set = set(rad_I_colon_x_target)
                fast_contains_target = lambda y: y in target_set
            except TypeError:
                fast_contains_target = lambda y: contains(rad_I_colon_x_target, y)
                
            subset = all(fast_contains_target(r) for r in rad_I_colon_x)
            return not subset
        except Exception:
            return False

    return [safe_is_ideal(), safe_is_in_R(), safe_neg_q()]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: x is an element of R",
    "¬Q: \\sqrt{(I : x)} is not a subset of (\\sqrt{I} : x)"
]

N_HYP = 2
NEG_Q_INDEX = 2
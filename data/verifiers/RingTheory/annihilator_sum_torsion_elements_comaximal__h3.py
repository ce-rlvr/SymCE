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
O2 = zeros(2,2)
O3 = zeros(3,3)

# Note: The witness must be a finite counterexample.
# Please provide a witness object with the following attributes:
# - R_elements: list of elements in the ring R
# - M_elements: list of elements in the module M
# - R_add(a, b): function for addition in R
# - R_mul(a, b): function for multiplication in R
# - M_add(a, b): function for addition in M
# - action(r, m): function for R-action on M
# - x: element of M
# - y: element of M
# Alternatively, provide tables: R_add, R_mul, M_add, action (as 2D lists) and x, y as integers.

class Witness:
    def __init__(self, R_elements, M_elements, R_add, R_mul, M_add, action, x, y):
        self.R_elements = R_elements
        self.M_elements = M_elements
        self.R_add = R_add
        self.R_mul = R_mul
        self.M_add = M_add
        self.action = action
        self.x = x
        self.y = y

def contains(lst, item):
    for x in lst:
        if x == item:
            return True
    return False

def find_zero(elements, add_func):
    for e in elements:
        is_zero = True
        for a in elements:
            if add_func(e, a) != a:
                is_zero = False
                break
        if is_zero:
            return e
    return None

def extract(w):
    if isinstance(w, dict):
        class Dummy: pass
        obj = Dummy()
        for k, v in w.items():
            setattr(obj, k, v)
        w = obj

    if hasattr(w, 'R_add') and isinstance(w.R_add, list) and not callable(w.R_add):
        R_elements = list(range(len(w.R_add)))
        M_elements = list(range(len(w.M_add)))
        R_add = lambda a, b: w.R_add[a][b]
        R_mul = lambda a, b: w.R_mul[a][b]
        M_add = lambda a, b: w.M_add[a][b]
        action = lambda r, m: w.action[r][m]
        x = w.x
        y = w.y
    else:
        R_elements = list(w.R_elements)
        M_elements = list(w.M_elements)
        R_add = w.R_add
        R_mul = w.R_mul
        M_add = w.M_add
        action = w.action
        x = w.x
        y = w.y

    zero_R = find_zero(R_elements, R_add)
    zero_M = find_zero(M_elements, M_add)
    
    return R_elements, M_elements, R_add, R_mul, M_add, action, x, y, zero_R, zero_M

def check_H1(w):
    R_elements, M_elements, R_add, R_mul, M_add, action, x, y, zero_R, zero_M = extract(w)
    if zero_R is None: return False
    
    for a in R_elements:
        for b in R_elements:
            c = R_add(a, b)
            if not contains(R_elements, c): return False
            if R_add(a, b) != R_add(b, a): return False
            
    for a in R_elements:
        for b in R_elements:
            for c in R_elements:
                if R_add(R_add(a, b), c) != R_add(a, R_add(b, c)): return False
                
    for a in R_elements:
        has_inv = False
        for b in R_elements:
            if R_add(a, b) == zero_R:
                has_inv = True
                break
        if not has_inv: return False
        
    for a in R_elements:
        for b in R_elements:
            c = R_mul(a, b)
            if not contains(R_elements, c): return False
            if R_mul(a, b) != R_mul(b, a): return False
            
    for a in R_elements:
        for b in R_elements:
            for c in R_elements:
                if R_mul(R_mul(a, b), c) != R_mul(a, R_mul(b, c)): return False
                
    for a in R_elements:
        for b in R_elements:
            for c in R_elements:
                if R_mul(a, R_add(b, c)) != R_add(R_mul(a, b), R_mul(a, c)): return False
                
    return True

def check_H2(w):
    R_elements, M_elements, R_add, R_mul, M_add, action, x, y, zero_R, zero_M = extract(w)
    if zero_M is None: return False
    
    if not contains(M_elements, x): return False
    if not contains(M_elements, y): return False
    
    for a in M_elements:
        for b in M_elements:
            c = M_add(a, b)
            if not contains(M_elements, c): return False
            if M_add(a, b) != M_add(b, a): return False
            
    for a in M_elements:
        for b in M_elements:
            for c in M_elements:
                if M_add(M_add(a, b), c) != M_add(a, M_add(b, c)): return False
                
    for a in M_elements:
        has_inv = False
        for b in M_elements:
            if M_add(a, b) == zero_M:
                has_inv = True
                break
        if not has_inv: return False
        
    for r in R_elements:
        for m in M_elements:
            if not contains(M_elements, action(r, m)): return False
            
    for r in R_elements:
        for m1 in M_elements:
            for m2 in M_elements:
                if action(r, M_add(m1, m2)) != M_add(action(r, m1), action(r, m2)): return False
                
    for r1 in R_elements:
        for r2 in R_elements:
            for m in M_elements:
                if action(R_add(r1, r2), m) != M_add(action(r1, m), action(r2, m)): return False
                
    for r1 in R_elements:
        for r2 in R_elements:
            for m in M_elements:
                if action(R_mul(r1, r2), m) != action(r1, action(r2, m)): return False
                
    return True

def check_H3(w):
    R_elements, M_elements, R_add, R_mul, M_add, action, x, y, zero_R, zero_M = extract(w)
    
    Ann_x = [r for r in R_elements if action(r, x) == zero_M]
    Ann_y = [r for r in R_elements if action(r, y) == zero_M]
    
    sum_ideal = []
    for a in Ann_x:
        for b in Ann_y:
            s = R_add(a, b)
            if not contains(sum_ideal, s):
                sum_ideal.append(s)
                
    for r in R_elements:
        if not contains(sum_ideal, r): return False
    return True

def check_neg_Q(w):
    R_elements, M_elements, R_add, R_mul, M_add, action, x, y, zero_R, zero_M = extract(w)
    
    Ann_x = [r for r in R_elements if action(r, x) == zero_M]
    Ann_y = [r for r in R_elements if action(r, y) == zero_M]
    
    xy = M_add(x, y)
    Ann_xy = [r for r in R_elements if action(r, xy) == zero_M]
    
    intersection = [r for r in Ann_x if contains(Ann_y, r)]
    
    for r in Ann_xy:
        if not contains(intersection, r): return True
    for r in intersection:
        if not contains(Ann_xy, r): return True
        
    return False

def conditions(witness):
    try:
        H1 = check_H1(witness)
    except Exception:
        H1 = False
        
    try:
        H2 = check_H2(witness)
    except Exception:
        H2 = False
        
    try:
        H3 = check_H3(witness)
    except Exception:
        H3 = False
        
    try:
        neg_Q = check_neg_Q(witness)
    except Exception:
        neg_Q = False
        
    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is an R-module",
    "H_3: The annihilator ideals Ann_R(x) and Ann_R(y) are comaximal in R",
    "¬Q: Ann_R(x+y) is not equal to Ann_R(x) ∩ Ann_R(y)"
]

N_HYP = 3
NEG_Q_INDEX = 3
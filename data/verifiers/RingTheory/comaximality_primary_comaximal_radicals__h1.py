import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Standard algebra objects
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

def get_attr_or_key(obj, key, default=None):
    try:
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)
    except Exception:
        return default

def check_ideal(elements, add, mul, zero, I):
    if not all(x in elements for x in I): return False
    if zero not in I: return False
    for x in I:
        for y in I:
            if add(x, y) not in I: return False
    for x in I:
        inv_x = None
        for y in elements:
            if add(x, y) == zero and add(y, x) == zero:
                inv_x = y
                break
        if inv_x not in I: return False
    for r in elements:
        for x in I:
            if mul(r, x) not in I: return False
            if mul(x, r) not in I: return False
    return True

def check_primary(elements, add, mul, zero, Q):
    if not check_ideal(elements, add, mul, zero, Q): return False
    if len(Q) == len(elements) and all(x in Q for x in elements): return False
    
    for a in elements:
        for b in elements:
            if mul(a, b) in Q:
                if a not in Q:
                    b_n = b
                    found = False
                    for n in range(1, len(elements) + 2):
                        if b_n in Q:
                            found = True
                            break
                        b_n = mul(b_n, b)
                    if not found:
                        return False
    return True

def get_radical(elements, mul, Q):
    rad = []
    for x in elements:
        x_n = x
        for n in range(1, len(elements) + 2):
            if x_n in Q:
                rad.append(x)
                break
            x_n = mul(x_n, x)
    return rad

def get_sum(add, A, B):
    res = []
    for a in A:
        for b in B:
            res.append(add(a, b))
    unique = []
    for x in res:
        if x not in unique:
            unique.append(x)
    return unique

def conditions(witness):
    try:
        elements = get_attr_or_key(witness, 'elements')
        add = get_attr_or_key(witness, 'add')
        mul = get_attr_or_key(witness, 'mul')
        zero = get_attr_or_key(witness, 'zero')
        Q1 = get_attr_or_key(witness, 'Q1')
        Q2 = get_attr_or_key(witness, 'Q2')
        
        if elements is None or add is None or mul is None or zero is None or Q1 is None or Q2 is None:
            return [False, False, False]
            
        unique_elements = []
        for x in elements:
            if x not in unique_elements:
                unique_elements.append(x)
        if len(unique_elements) != len(elements):
            return [False, False, False]
            
        if zero not in elements:
            return [False, False, False]
            
        # Check if it's a valid ring
        is_ring = True
        for a in elements:
            for b in elements:
                if add(a, b) not in elements: is_ring = False
                if mul(a, b) not in elements: is_ring = False
        if not is_ring: return [False, False, False]
        
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a: is_ring = False
            for b in elements:
                if add(a, b) != add(b, a): is_ring = False
                for c in elements:
                    if add(a, add(b, c)) != add(add(a, b), c): is_ring = False
        for a in elements:
            inv_found = False
            for b in elements:
                if add(a, b) == zero:
                    inv_found = True
                    break
            if not inv_found: is_ring = False
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul(a, mul(b, c)) != mul(mul(a, b), c): is_ring = False
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): is_ring = False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): is_ring = False
        
        if not is_ring:
            return [False, False, False]
            
        # H_1: Q_1 and Q_2 are primary ideals of R
        h1 = check_primary(elements, add, mul, zero, Q1) and check_primary(elements, add, mul, zero, Q2)
        
        # H_2: The radicals \sqrt{Q_1} and \sqrt{Q_2} are comaximal
        rad_Q1 = get_radical(elements, mul, Q1)
        rad_Q2 = get_radical(elements, mul, Q2)
        sum_rad = get_sum(add, rad_Q1, rad_Q2)
        h2 = (len(sum_rad) == len(elements)) and all(x in sum_rad for x in elements)
        
        # ¬Q: The primary ideals Q_1 and Q_2 are not comaximal
        sum_Q = get_sum(add, Q1, Q2)
        neg_q = len(sum_Q) != len(elements) or any(x not in sum_Q for x in elements)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: Q_1 and Q_2 are primary ideals of R",
    "H_2: The radicals \\sqrt{Q_1} and \\sqrt{Q_2} are comaximal, satisfying \\sqrt{Q_1} + \\sqrt{Q_2} = R",
    "¬Q: The primary ideals Q_1 and Q_2 are not comaximal (Q_1 + Q_2 != R)"
]

N_HYP = 2
NEG_Q_INDEX = 2
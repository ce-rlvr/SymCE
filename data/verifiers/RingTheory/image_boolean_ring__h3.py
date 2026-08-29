import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import itertools
import functools
import math

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

def get_val(op, a, b):
    if isinstance(op, dict):
        return op[(a, b)]
    return op(a, b)

def get_f(f, a):
    if isinstance(f, dict):
        return f[a]
    return f(a)

def is_ring(elements, add, mul):
    if not elements: return False
    
    def a(x, y): return get_val(add, x, y)
    def m(x, y): return get_val(mul, x, y)
    
    # closure
    for x in elements:
        for y in elements:
            if a(x, y) not in elements: return False
            if m(x, y) not in elements: return False
            
    # add commutativity & associativity
    for x in elements:
        for y in elements:
            if a(x, y) != a(y, x): return False
            for z in elements:
                if a(a(x, y), z) != a(x, a(y, z)): return False
                
    # zero
    zeros_list = [z for z in elements if all(a(x, z) == x for x in elements)]
    if not zeros_list: return False
    zero = zeros_list[0]
    
    # inverses
    for x in elements:
        if not any(a(x, y) == zero for y in elements): return False
        
    # mul associativity & distributivity
    for x in elements:
        for y in elements:
            for z in elements:
                if m(m(x, y), z) != m(x, m(y, z)): return False
                if m(x, a(y, z)) != a(m(x, y), m(x, z)): return False
                if m(a(x, y), z) != a(m(x, z), m(y, z)): return False
                
    return True

def is_boolean_ring(elements, add, mul):
    if not is_ring(elements, add, mul): return False
    def m(x, y): return get_val(mul, x, y)
    for x in elements:
        if m(x, x) != x: return False
    return True

def get_zero(elements, add):
    def a(x, y): return get_val(add, x, y)
    zeros_list = [z for z in elements if all(a(x, z) == x for x in elements)]
    return zeros_list[0] if zeros_list else None

def is_subring(img, S_elements, S_add, S_mul):
    if not img: return False
    if not all(x in S_elements for x in img): return False
    
    def a(x, y): return get_val(S_add, x, y)
    def m(x, y): return get_val(S_mul, x, y)
    
    # closure
    for x in img:
        for y in img:
            if a(x, y) not in img: return False
            if m(x, y) not in img: return False
            
    zero = get_zero(S_elements, S_add)
    if zero not in img: return False
    
    # inverses in img
    for x in img:
        if not any(a(x, y) == zero for y in img): return False
        
    return True

def is_boolean_subring(img, S_elements, S_add, S_mul):
    if not is_subring(img, S_elements, S_add, S_mul): return False
    def m(x, y): return get_val(S_mul, x, y)
    for x in img:
        if m(x, x) != x: return False
    return True

def image(elements, f):
    img = []
    for x in elements:
        y = get_f(f, x)
        if y not in img:
            img.append(y)
    return img

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R_elements = list(witness["R_elements"])
            R_add = witness["R_add"]
            R_mul = witness["R_mul"]
            S_elements = list(witness["S_elements"])
            S_add = witness["S_add"]
            S_mul = witness["S_mul"]
            f = witness["f"]
        elif isinstance(witness, (list, tuple)) and len(witness) == 7:
            R_elements = list(witness[0])
            R_add = witness[1]
            R_mul = witness[2]
            S_elements = list(witness[3])
            S_add = witness[4]
            S_mul = witness[5]
            f = witness[6]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: R is a Boolean ring
    try:
        h1 = is_boolean_ring(R_elements, R_add, R_mul)
    except Exception:
        h1 = False
        
    # H2: S is a ring
    try:
        h2 = is_ring(S_elements, S_add, S_mul)
    except Exception:
        h2 = False
        
    # neg_Q: Image of R under f is NOT a Boolean subring of S
    try:
        img = image(R_elements, f)
        q = is_boolean_subring(img, S_elements, S_add, S_mul)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: S is a ring",
    "¬Q: The image of R under f is not a Boolean subring of S"
]

N_HYP = 2
NEG_Q_INDEX = 2
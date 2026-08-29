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

def unique_elements(elements):
    res = []
    for e in elements:
        if e not in res:
            res.append(e)
    return res

def call_op(op, a, b):
    if isinstance(op, dict):
        return op[(a, b)]
    return op(a, b)

def call_f(f, a):
    if isinstance(f, dict):
        return f[a]
    return f(a)

def is_comm_ring_with_id(elements, add, mul):
    elements = unique_elements(elements)
    if not elements: 
        return False, None, None
    
    # Closure
    for a in elements:
        for b in elements:
            if call_op(add, a, b) not in elements: return False, None, None
            if call_op(mul, a, b) not in elements: return False, None, None
            
    # Addition associativity and commutativity
    for a in elements:
        for b in elements:
            if call_op(add, a, b) != call_op(add, b, a): return False, None, None
            for c in elements:
                if call_op(add, call_op(add, a, b), c) != call_op(add, a, call_op(add, b, c)): return False, None, None
                
    # Additive identity
    zero = None
    for e in elements:
        if all(call_op(add, e, a) == a for a in elements):
            zero = e
            break
    if zero is None: return False, None, None
    
    # Additive inverses
    for a in elements:
        if not any(call_op(add, a, b) == zero for b in elements): return False, None, None
        
    # Multiplication associativity and commutativity
    for a in elements:
        for b in elements:
            if call_op(mul, a, b) != call_op(mul, b, a): return False, None, None
            for c in elements:
                if call_op(mul, call_op(mul, a, b), c) != call_op(mul, a, call_op(mul, b, c)): return False, None, None
                
    # Multiplicative identity
    one = None
    for e in elements:
        if all(call_op(mul, e, a) == a for a in elements):
            one = e
            break
    if one is None: return False, None, None
    
    # Distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if call_op(mul, a, call_op(add, b, c)) != call_op(add, call_op(mul, a, b), call_op(mul, a, c)): return False, None, None
                
    return True, zero, one

def is_boolean_ring(elements, add, mul):
    elements = unique_elements(elements)
    if not elements: 
        return False, None
        
    # Closure
    for a in elements:
        for b in elements:
            if call_op(add, a, b) not in elements: return False, None
            if call_op(mul, a, b) not in elements: return False, None
            
    # Addition associativity and commutativity
    for a in elements:
        for b in elements:
            if call_op(add, a, b) != call_op(add, b, a): return False, None
            for c in elements:
                if call_op(add, call_op(add, a, b), c) != call_op(add, a, call_op(add, b, c)): return False, None
                
    # Additive identity
    zero = None
    for e in elements:
        if all(call_op(add, e, a) == a for a in elements):
            zero = e
            break
    if zero is None: return False, None
    
    # Additive inverses
    for a in elements:
        if not any(call_op(add, a, b) == zero for b in elements): return False, None
        
    # Multiplication associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if call_op(mul, call_op(mul, a, b), c) != call_op(mul, a, call_op(mul, b, c)): return False, None
                
    # Distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if call_op(mul, a, call_op(add, b, c)) != call_op(add, call_op(mul, a, b), call_op(mul, a, c)): return False, None
                if call_op(mul, call_op(add, b, c), a) != call_op(add, call_op(mul, b, a), call_op(mul, c, a)): return False, None
                
    # Boolean property
    for a in elements:
        if call_op(mul, a, a) != a: return False, None
        
    return True, zero

def get_neg(elements, add, zero, x):
    for y in elements:
        if call_op(add, x, y) == zero:
            return y
    return None

def get_ideal(elements, add, mul, zero, S):
    ideal = []
    for s in S:
        if s not in ideal:
            ideal.append(s)
    changed = True
    while changed:
        changed = False
        new_elements = []
        for x in ideal:
            neg_x = get_neg(elements, add, zero, x)
            if neg_x is not None and neg_x not in ideal and neg_x not in new_elements:
                new_elements.append(neg_x)
            for y in ideal:
                res = call_op(add, x, y)
                if res not in ideal and res not in new_elements:
                    new_elements.append(res)
            for r in elements:
                res1 = call_op(mul, r, x)
                if res1 not in ideal and res1 not in new_elements:
                    new_elements.append(res1)
                res2 = call_op(mul, x, r)
                if res2 not in ideal and res2 not in new_elements:
                    new_elements.append(res2)
        if new_elements:
            ideal.extend(new_elements)
            changed = True
    return ideal

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R_elements = witness['R_elements']
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            B_elements = witness['B_elements']
            B_add = witness['B_add']
            B_mul = witness['B_mul']
            f = witness['f']
        else:
            R_elements = witness.R_elements
            R_add = witness.R_add
            R_mul = witness.R_mul
            B_elements = witness.B_elements
            B_add = witness.B_add
            B_mul = witness.B_mul
            f = witness.f
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring with identity
    try:
        h1_ok, R_zero, R_one = is_comm_ring_with_id(R_elements, R_add, R_mul)
    except Exception:
        h1_ok = False

    # H2: B is a Boolean ring
    try:
        h2_ok, B_zero = is_boolean_ring(B_elements, B_add, B_mul)
    except Exception:
        h2_ok = False

    # ¬Q: The kernel of f does not contain the ideal generated by {x^2 - x | x in R}
    neg_q_ok = False
    try:
        if h1_ok and h2_ok:
            gens = []
            for x in unique_elements(R_elements):
                x2 = call_op(R_mul, x, x)
                neg_x = get_neg(R_elements, R_add, R_zero, x)
                gen = call_op(R_add, x2, neg_x)
                if gen not in gens:
                    gens.append(gen)
            
            ideal = get_ideal(unique_elements(R_elements), R_add, R_mul, R_zero, gens)
            
            ideal_in_kernel = True
            for x in ideal:
                if call_f(f, x) != B_zero:
                    ideal_in_kernel = False
                    break
            
            neg_q_ok = not ideal_in_kernel
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: B is a Boolean ring",
    "¬Q: The kernel of f does not contain the ideal generated by {x^2 - x | x in R}"
]

N_HYP = 2
NEG_Q_INDEX = 2
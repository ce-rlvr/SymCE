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

def check_set_eq(list1, list2):
    for x in list1:
        if x not in list2: return False
    for x in list2:
        if x not in list1: return False
    return True

def get_op(op):
    if isinstance(op, dict):
        return lambda a, b: op[(a, b)]
    return op

def get_map(m):
    if isinstance(m, dict):
        return lambda a: m[a]
    return m

def is_commutative_ring_with_identity(elements, add, mul, zero, one):
    if zero not in elements or one not in elements: return False
    for a in elements:
        if add(a, zero) != a or add(zero, a) != a: return False
        if mul(a, one) != a or mul(one, a) != a: return False
        
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
        for b in elements:
            if add(a, b) not in elements: return False
            if mul(a, b) not in elements: return False
            if add(a, b) != add(b, a): return False
            if mul(a, b) != mul(b, a): return False
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
    return True

def is_ideal(elements, add, mul, zero, ideal_elements):
    if zero not in ideal_elements: return False
    for q in ideal_elements:
        if q not in elements: return False
        has_inv = False
        for b in ideal_elements:
            if add(q, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
        for p in ideal_elements:
            if add(q, p) not in ideal_elements: return False
        for r in elements:
            if mul(r, q) not in ideal_elements: return False
    return True

def radical(elements, mul, ideal_elements):
    rad = []
    for a in elements:
        curr = a
        is_in_rad = False
        for n in range(1, len(elements) + 2):
            if curr in ideal_elements:
                is_in_rad = True
                break
            curr = mul(curr, a)
        if is_in_rad:
            rad.append(a)
    return rad

def is_primary_ideal(elements, add, mul, zero, Q_elements, P_elements):
    if not is_ideal(elements, add, mul, zero, Q_elements): return False
    if not is_ideal(elements, add, mul, zero, P_elements): return False
    
    if check_set_eq(elements, Q_elements): return False
    
    rad_Q = radical(elements, mul, Q_elements)
    if not check_set_eq(P_elements, rad_Q): return False
    
    for a in elements:
        for b in elements:
            if mul(a, b) in Q_elements:
                if a not in Q_elements and b not in P_elements:
                    return False
    return True

def conditions(witness):
    try:
        R = witness['R']
        S = witness['S']
        add_R = get_op(witness['add_R'])
        mul_R = get_op(witness['mul_R'])
        add_S = get_op(witness['add_S'])
        mul_S = get_op(witness['mul_S'])
        zero_R = witness['zero_R']
        one_R = witness['one_R']
        zero_S = witness['zero_S']
        one_S = witness['one_S']
        f = get_map(witness['f'])
        Q = witness['Q']
        P = witness['P']
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_commutative_ring_with_identity(R, add_R, mul_R, zero_R, one_R) and \
             is_commutative_ring_with_identity(S, add_S, mul_S, zero_S, one_S)
    except Exception:
        h1 = False

    try:
        h2 = is_primary_ideal(S, add_S, mul_S, zero_S, Q, P)
    except Exception:
        h2 = False

    try:
        f_inv_Q = [r for r in R if f(r) in Q]
        f_inv_P = [r for r in R if f(r) in P]
        is_primary = is_primary_ideal(R, add_R, mul_R, zero_R, f_inv_Q, f_inv_P)
        neg_q = not is_primary
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: Q is a P-primary ideal of S",
    "¬Q: The contraction f^{-1}(Q) is not an f^{-1}(P)-primary ideal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2
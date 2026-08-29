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

def check_field(F, add_F, mul_F, zero_F, one_F):
    if len(F) < 2: return False
    if zero_F == one_F: return False
    if zero_F not in F or one_F not in F: return False
    for a in F:
        if add_F(a, zero_F) != a or add_F(zero_F, a) != a: return False
        if mul_F(a, one_F) != a or mul_F(one_F, a) != a: return False
        has_add_inv = any(add_F(a, b) == zero_F and add_F(b, a) == zero_F for b in F)
        if not has_add_inv: return False
        if a != zero_F:
            has_mul_inv = any(mul_F(a, b) == one_F and mul_F(b, a) == one_F for b in F)
            if not has_mul_inv: return False
        for b in F:
            if add_F(a, b) not in F: return False
            if mul_F(a, b) not in F: return False
            if add_F(a, b) != add_F(b, a): return False
            if mul_F(a, b) != mul_F(b, a): return False
            for c in F:
                if add_F(add_F(a, b), c) != add_F(a, add_F(b, c)): return False
                if mul_F(mul_F(a, b), c) != mul_F(a, mul_F(b, c)): return False
                if mul_F(a, add_F(b, c)) != add_F(mul_F(a, b), mul_F(a, c)): return False
                if mul_F(add_F(a, b), c) != add_F(mul_F(a, c), mul_F(b, c)): return False
    return True

def check_ring_hom(F, S, add_F, mul_F, add_S, mul_S, zero_S, one_S, one_F, f):
    if zero_S not in S or one_S not in S: return False
    for a in S:
        if add_S(a, zero_S) != a or add_S(zero_S, a) != a: return False
        if mul_S(a, one_S) != a or mul_S(one_S, a) != a: return False
        has_add_inv = any(add_S(a, b) == zero_S and add_S(b, a) == zero_S for b in S)
        if not has_add_inv: return False
        for b in S:
            if add_S(a, b) not in S: return False
            if mul_S(a, b) not in S: return False
            if add_S(a, b) != add_S(b, a): return False
            for c in S:
                if add_S(add_S(a, b), c) != add_S(a, add_S(b, c)): return False
                if mul_S(mul_S(a, b), c) != mul_S(a, mul_S(b, c)): return False
                if mul_S(a, add_S(b, c)) != add_S(mul_S(a, b), mul_S(a, c)): return False
                if mul_S(add_S(a, b), c) != add_S(mul_S(a, c), mul_S(b, c)): return False
    
    if f(one_F) != one_S: return False
    for a in F:
        if f(a) not in S: return False
        for b in F:
            if f(add_F(a, b)) != add_S(f(a), f(b)): return False
            if f(mul_F(a, b)) != mul_S(f(a), f(b)): return False
    return True

def check_not_injective(F, f):
    for a in F:
        for b in F:
            if a != b and f(a) == f(b):
                return True
    return False

def conditions(witness):
    try:
        F = list(witness['F'])
        add_F = witness['add_F']
        mul_F = witness['mul_F']
        zero_F = witness['zero_F']
        one_F = witness['one_F']
        h1 = check_field(F, add_F, mul_F, zero_F, one_F)
    except Exception:
        h1 = False

    try:
        F = list(witness['F'])
        S = list(witness['S'])
        add_F = witness['add_F']
        mul_F = witness['mul_F']
        add_S = witness['add_S']
        mul_S = witness['mul_S']
        zero_S = witness['zero_S']
        one_S = witness['one_S']
        one_F = witness['one_F']
        f = witness['f']
        h2 = check_ring_hom(F, S, add_F, mul_F, add_S, mul_S, zero_S, one_S, one_F, f)
    except Exception:
        h2 = False

    try:
        F = list(witness['F'])
        f = witness['f']
        neg_q = check_not_injective(F, f)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a ring homomorphism from F to S",
    "¬Q: f is not an injective ring homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2
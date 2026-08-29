import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

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

def is_zero(c):
    try:
        if hasattr(c, 'is_zero_matrix'):
            return bool(c.is_zero_matrix)
        if hasattr(c, 'is_zero') and c.is_zero is not None:
            return bool(c.is_zero)
        if hasattr(c, 'expand'):
            expanded = c.expand()
            if hasattr(expanded, 'is_zero_matrix') and expanded.is_zero_matrix:
                return True
            if hasattr(expanded, 'is_zero') and expanded.is_zero is not None:
                return bool(expanded.is_zero)
            return bool(expanded == 0)
        eq = (c == 0)
        if hasattr(eq, 'all'):
            return bool(eq.all())
        return bool(eq)
    except Exception:
        return False

def is_zero_poly(p):
    for c in p:
        if not is_zero(c):
            return False
    return True

def poly_mul(p, q):
    if not p or not q:
        return []
    try:
        zero = p[0] - p[0]
    except Exception:
        zero = p[0] * 0
        
    if hasattr(zero, 'expand'):
        zero = zero.expand()
        
    res = [zero] * (len(p) + len(q) - 1)
    for i in range(len(p)):
        for j in range(len(q)):
            term = p[i] * q[j]
            res[i+j] = res[i+j] + term
            
    for k in range(len(res)):
        if hasattr(res[k], 'expand'):
            res[k] = res[k].expand()
    return res

def is_nilpotent_poly(p, max_squarings=6):
    if is_zero_poly(p):
        return True
    curr = p
    for _ in range(max_squarings):
        curr = poly_mul(curr, curr)
        if is_zero_poly(curr):
            return True
    return False

def is_nilpotent_element(c, max_squarings=6):
    if is_zero(c):
        return True
    curr = c
    for _ in range(max_squarings):
        curr = curr * curr
        if hasattr(curr, 'expand'):
            curr = curr.expand()
        if is_zero(curr):
            return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            h1 = True
            coeffs = list(witness)
        elif hasattr(witness, 'all_coeffs'):
            h1 = True
            coeffs = witness.all_coeffs()
        else:
            h1 = False
            coeffs = []
    except Exception:
        h1 = False
        coeffs = []

    try:
        h2 = False
        if h1:
            h2 = is_nilpotent_poly(coeffs, max_squarings=6)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1:
            for c in coeffs:
                if not is_nilpotent_element(c, max_squarings=6):
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial",
    "H_2: f is a nilpotent element in the polynomial ring",
    "¬Q: At least one coefficient of f is not nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2
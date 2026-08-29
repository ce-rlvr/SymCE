import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
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

def is_zero(x):
    try:
        if hasattr(x, 'is_zero_matrix'):
            return x.is_zero_matrix
        if hasattr(x, 'is_zero'):
            return x.is_zero
        return bool(x == 0)
    except Exception:
        return False

def is_non_zero(x):
    try:
        if hasattr(x, 'is_zero_matrix'):
            return not x.is_zero_matrix
        if hasattr(x, 'is_zero'):
            return not x.is_zero
        return bool(x != 0)
    except Exception:
        return False

def is_nilpotent(x):
    try:
        if hasattr(x, 'is_nilpotent'):
            if callable(x.is_nilpotent):
                return x.is_nilpotent()
            return x.is_nilpotent
        if hasattr(x, 'shape') and len(x.shape) == 2 and x.shape[0] == x.shape[1]:
            n = x.shape[0]
            xn = x**n
            return is_zero(xn)
        
        p = x
        for _ in range(100):
            try:
                p = p * x
            except Exception:
                break
            if is_zero(p):
                return True
        return False
    except Exception:
        return False

def is_zero_divisor(x):
    try:
        if hasattr(x, 'is_zero_divisor'):
            if callable(x.is_zero_divisor):
                return x.is_zero_divisor()
            return x.is_zero_divisor
        if hasattr(x, 'det'):
            return x.det() == 0 and is_non_zero(x)
        
        # Constructive check for left/right zero divisors in associative/non-associative rings
        p = x
        prev = x
        for _ in range(1, 100):
            if is_zero(p):
                if is_non_zero(prev):
                    return True
            prev = p
            try:
                p = p * x
            except Exception:
                break
            
        p = x
        prev = x
        for _ in range(1, 100):
            if is_zero(p):
                if is_non_zero(prev):
                    return True
            prev = p
            try:
                p = x * p
            except Exception:
                break
            
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        h1 = is_non_zero(witness)
    except Exception:
        h1 = False

    try:
        h2 = is_nilpotent(witness)
    except Exception:
        h2 = False

    try:
        neg_q = not is_zero_divisor(witness)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x is a non-zero element of R",
    "H_2: x is a nilpotent element",
    "not Q: x is not a zero divisor in R"
]

N_HYP = 2
NEG_Q_INDEX = 2
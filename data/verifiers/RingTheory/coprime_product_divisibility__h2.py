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

def get_zero(R):
    if hasattr(R, 'zero'): return R.zero
    return 0

def get_one(R):
    if hasattr(R, 'one'): return R.one
    return 1

def divides(R, divisor, dividend):
    zero = get_zero(R)
    try:
        if divisor == zero or divisor == 0:
            return dividend == zero or dividend == 0
    except Exception:
        pass

    if hasattr(R, 'div'):
        try:
            return R.div(dividend, divisor)[1] in (zero, 0)
        except Exception:
            pass

    try:
        from sympy import div
        return div(dividend, divisor, domain=R)[1] in (zero, 0)
    except Exception:
        pass

    try:
        return (dividend % divisor) in (zero, 0)
    except Exception:
        pass

    try:
        q, r = divmod(dividend, divisor)
        return r in (zero, 0)
    except Exception:
        pass

    return False

def is_coprime(R, a, b):
    try:
        g = None
        if hasattr(R, 'gcd'):
            try:
                g = R.gcd(a, b)
            except Exception:
                pass
        if g is None:
            from sympy import gcd
            g = gcd(a, b)
        
        one = get_one(R)
        return divides(R, g, one)
    except Exception:
        return False

def multiply(R, a, b):
    if hasattr(R, 'mul'):
        try:
            return R.mul(a, b)
        except Exception:
            pass
    return a * b

def is_ufd(R):
    try:
        if hasattr(R, 'is_UFD'):
            return bool(R.is_UFD)
        if hasattr(R, 'is_ufd'):
            return bool(R.is_ufd)
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False, False, False]
        R, a, b, c = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        h1 = is_ufd(R)
    except Exception:
        h1 = False

    try:
        h2 = is_coprime(R, a, b)
    except Exception:
        h2 = False

    try:
        h3 = divides(R, a, c)
    except Exception:
        h3 = False

    try:
        h4 = divides(R, b, c)
    except Exception:
        h4 = False

    try:
        ab = multiply(R, a, b)
        neg_q = not divides(R, ab, c)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a and b are coprime (gcd is a unit)",
    "H_3: a divides c in R",
    "H_4: b divides c in R",
    "¬Q: ab does not divide c in R"
]

N_HYP = 4
NEG_Q_INDEX = 4
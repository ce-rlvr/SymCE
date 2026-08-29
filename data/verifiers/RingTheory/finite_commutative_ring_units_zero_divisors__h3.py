import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def eq(a, b):
    try:
        return bool(a == b)
    except Exception:
        return False

def neq(a, b):
    return not eq(a, b)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, x = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        if hasattr(R, 'elements'):
            if callable(R.elements):
                elem_iter = R.elements()
            else:
                elem_iter = R.elements
            
            elements = []
            for i, e in enumerate(elem_iter):
                if i > 2000:
                    return [False, False, False, False]
                elements.append(e)
            zero = R.zero
            add = R.add
            mul = R.mul
        elif isinstance(R, tuple) and len(R) == 4:
            elements = list(R[0])
            if isinstance(R[1], dict):
                add = lambda a, b: R[1][(a, b)]
                mul = lambda a, b: R[2][(a, b)]
            else:
                add = R[1]
                mul = R[2]
            zero = R[3]
        else:
            return [False, False, False, False]
            
        if not (callable(add) and callable(mul)):
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = len(elements) > 0 and any(eq(e, zero) for e in elements)
        if h1 and len(elements) <= 100:
            for a in elements:
                if neq(add(a, zero), a): h1 = False
                if neq(add(zero, a), a): h1 = False
    except Exception:
        h1 = False

    try:
        h2 = True
        for a in elements:
            for b in elements:
                if neq(mul(a, b), mul(b, a)):
                    h2 = False
                    break
            if not h2: break
    except Exception:
        h2 = False

    try:
        h3 = any(eq(e, x) for e in elements) and neq(x, zero)
    except Exception:
        h3 = False

    try:
        ones = []
        for e in elements:
            is_id = True
            for a in elements:
                if neq(mul(e, a), a) or neq(mul(a, e), a):
                    is_id = False
                    break
            if is_id:
                ones.append(e)
        
        is_unit = False
        if ones:
            one = ones[0]
            for y in elements:
                if eq(mul(x, y), one) and eq(mul(y, x), one):
                    is_unit = True
                    break
                    
        is_zero_div = False
        for y in elements:
            if neq(y, zero):
                if eq(mul(x, y), zero) or eq(mul(y, x), zero):
                    is_zero_div = True
                    break
                    
        neg_q = not (is_unit or is_zero_div)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a finite ring",
    "H_2: R is a commutative ring",
    "H_3: x is a non-zero element of R",
    "¬Q: x is neither a unit nor a zero divisor in R"
]

N_HYP = 3
NEG_Q_INDEX = 3
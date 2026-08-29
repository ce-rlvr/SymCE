import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import itertools
import functools
import math

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

def eq(a, b):
    try:
        return bool(a == b)
    except Exception:
        return False

def contains(lst, item):
    for x in lst:
        if eq(x, item):
            return True
    return False

def get_zero(elements):
    for z in elements:
        is_z = True
        for a in elements:
            try:
                if not eq(a + z, a) or not eq(z + a, a):
                    is_z = False
                    break
            except Exception:
                is_z = False
                break
        if is_z:
            return z
    return None

def check_h1(elements, zero):
    try:
        for a in elements:
            has_inv = False
            for b in elements:
                try:
                    if eq(a + b, zero) and eq(b + a, zero):
                        has_inv = True
                        break
                except Exception:
                    pass
            if not has_inv: 
                return False
            
            for b in elements:
                try:
                    if not contains(elements, a + b): return False
                    if not contains(elements, a * b): return False
                    if not eq(a * b, b * a): return False
                except Exception:
                    return False
                    
        n = len(elements)
        if n <= 30:
            for a in elements:
                for b in elements:
                    for c in elements:
                        try:
                            if not eq((a + b) + c, a + (b + c)): return False
                            if not eq((a * b) * c, a * (b * c)): return False
                            if not eq(a * (b + c), a * b + a * c): return False
                        except Exception:
                            return False
        return True
    except Exception:
        return False

def check_neg_q(elements, zero):
    try:
        N = []
        for x in elements:
            curr = x
            is_nil = False
            for _ in range(len(elements)):
                if eq(curr, zero):
                    is_nil = True
                    break
                try:
                    curr = curr * x
                except Exception:
                    break
            if is_nil:
                N.append(x)
                
        if not N:
            return True
            
        for a in N:
            for b in N:
                if not contains(N, a + b):
                    return True
                    
        for a in N:
            for r in elements:
                if not contains(N, r * a):
                    return True
                if not contains(N, a * r):
                    return True
                    
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        elements = list(witness)
    except Exception:
        try:
            elements = list(witness.elements)
        except Exception:
            return [False, False]
            
    if not elements:
        return [False, False]
        
    zero = get_zero(elements)
    if zero is None:
        return [False, False]
        
    h1 = check_h1(elements, zero)
    neg_q = check_neg_q(elements, zero)
    
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: N is not an ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1
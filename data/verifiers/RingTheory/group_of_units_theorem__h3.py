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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(w):
    if hasattr(w, 'elements'): return w.elements
    return w['elements']

def get_zero(w):
    if hasattr(w, 'zero'): return w.zero
    return w['zero']

def get_one(w):
    if hasattr(w, 'one'): return w.one
    return w['one']

def call_add(w, a, b):
    if hasattr(w, 'add'): return w.add(a, b)
    return w['add'](a, b)

def call_mul(w, a, b):
    if hasattr(w, 'mul'): return w.mul(a, b)
    return w['mul'](a, b)

def conditions(witness) -> list[bool]:
    try:
        elements = get_elements(witness)
        zero = get_zero(witness)
        one = get_one(witness)
        elements_list = list(elements)
    except Exception:
        return [False, False, False]

    # H1: R is a ring (non-associative)
    h1 = True
    try:
        if zero not in elements_list:
            h1 = False
        else:
            for a in elements_list:
                if call_add(witness, a, zero) != a or call_add(witness, zero, a) != a:
                    h1 = False
                    break
                has_neg = False
                for b in elements_list:
                    if call_add(witness, a, b) == zero and call_add(witness, b, a) == zero:
                        has_neg = True
                        break
                if not has_neg:
                    h1 = False
                    break
                for b in elements_list:
                    ab_add = call_add(witness, a, b)
                    if ab_add not in elements_list:
                        h1 = False; break
                    ab_mul = call_mul(witness, a, b)
                    if ab_mul not in elements_list:
                        h1 = False; break
                    if ab_add != call_add(witness, b, a):
                        h1 = False; break
                    for c in elements_list:
                        if call_add(witness, a, call_add(witness, b, c)) != call_add(witness, ab_add, c):
                            h1 = False; break
                        bc_add = call_add(witness, b, c)
                        if call_mul(witness, a, bc_add) != call_add(witness, ab_mul, call_mul(witness, a, c)):
                            h1 = False; break
                        if call_mul(witness, ab_add, c) != call_add(witness, call_mul(witness, a, c), call_mul(witness, b, c)):
                            h1 = False; break
                    if not h1: break
                if not h1: break
    except Exception:
        h1 = False

    # H2: R has a multiplicative identity 1
    h2 = True
    try:
        if one not in elements_list:
            h2 = False
        else:
            for a in elements_list:
                if call_mul(witness, a, one) != a or call_mul(witness, one, a) != a:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: U(R) does NOT form a group under ring multiplication
    neg_q = False
    try:
        U = []
        for u in elements_list:
            is_unit = False
            for v in elements_list:
                if call_mul(witness, u, v) == one and call_mul(witness, v, u) == one:
                    is_unit = True
                    break
            if is_unit:
                U.append(u)
                
        is_group = True
        
        for a in U:
            for b in U:
                if call_mul(witness, a, b) not in U:
                    is_group = False
                    break
            if not is_group: break
            
        if is_group:
            for a in U:
                for b in U:
                    for c in U:
                        if call_mul(witness, a, call_mul(witness, b, c)) != call_mul(witness, call_mul(witness, a, b), c):
                            is_group = False
                            break
                    if not is_group: break
                if not is_group: break
                
        if is_group:
            if one not in U:
                is_group = False
            else:
                for a in U:
                    if call_mul(witness, a, one) != a or call_mul(witness, one, a) != a:
                        is_group = False
                        break
                        
        if is_group:
            for a in U:
                has_inv = False
                for b in U:
                    if call_mul(witness, a, b) == one and call_mul(witness, b, a) == one:
                        has_inv = True
                        break
                if not has_inv:
                    is_group = False
                    break
                    
        neg_q = not is_group
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R has a multiplicative identity 1",
    "¬Q: U(R) does not form a group under ring multiplication"
]

N_HYP = 2
NEG_Q_INDEX = 2
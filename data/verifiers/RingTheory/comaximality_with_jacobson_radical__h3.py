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

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is an ideal of R",
    "H_3: I and J(R) are comaximal",
    "¬Q: I is not the entire ring R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_ring_ops(witness):
    if isinstance(witness, dict):
        elements = list(witness.get('elements', []))
        add = witness.get('add')
        mul = witness.get('mul')
        zero = witness.get('zero')
        one = witness.get('one')
        I = list(witness.get('I', []))
        return elements, add, mul, zero, one, I
    else:
        elements = list(getattr(witness, 'elements', []))
        add = getattr(witness, 'add', None)
        mul = getattr(witness, 'mul', None)
        zero = getattr(witness, 'zero', None)
        one = getattr(witness, 'one', None)
        I = list(getattr(witness, 'I', []))
        return elements, add, mul, zero, one, I

def check_H1(elements, add, mul, zero, one):
    if not elements or not add or not mul: return False
    if zero not in elements: return False
    n = len(elements)
    if n > 100: return False
    
    for x in elements:
        if add(x, zero) != x or add(zero, x) != x: return False
        
    for x in elements:
        has_inv = False
        for y in elements:
            if add(x, y) == zero and add(y, x) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for x in elements:
        for y in elements:
            if add(x, y) != add(y, x): return False
            if mul(x, y) != mul(y, x): return False
            for z in elements:
                if add(add(x, y), z) != add(x, add(y, z)): return False
                if mul(mul(x, y), z) != mul(x, mul(y, z)): return False
                if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): return False
                if mul(add(x, y), z) != add(mul(x, z), mul(y, z)): return False
                
    if one not in elements: return False
    for x in elements:
        if mul(x, one) != x or mul(one, x) != x: return False
        
    return True

def get_add_inv(elements, add, zero, x):
    for y in elements:
        if add(x, y) == zero and add(y, x) == zero:
            return y
    return None

def get_JR(elements, add, mul, zero, one):
    JR = []
    for x in elements:
        in_JR = True
        for y in elements:
            xy = mul(x, y)
            neg_xy = get_add_inv(elements, add, zero, xy)
            if neg_xy is None:
                in_JR = False
                break
            one_minus_xy = add(one, neg_xy)
            
            is_unit = False
            for z in elements:
                if mul(one_minus_xy, z) == one and mul(z, one_minus_xy) == one:
                    is_unit = True
                    break
            if not is_unit:
                in_JR = False
                break
        if in_JR:
            JR.append(x)
    return JR

def check_H2(elements, add, mul, zero, I):
    if not I: return False
    for x in I:
        if x not in elements: return False
    
    if zero not in I: return False
    
    for x in I:
        for y in I:
            if add(x, y) not in I: return False
        inv_x = get_add_inv(elements, add, zero, x)
        if inv_x not in I: return False
        
    for x in I:
        for r in elements:
            if mul(r, x) not in I: return False
            if mul(x, r) not in I: return False
            
    return True

def check_H3(elements, add, mul, zero, one, I):
    JR = get_JR(elements, add, mul, zero, one)
    for i in I:
        for j in JR:
            if add(i, j) == one:
                return True
    return False

def check_neg_Q(elements, I):
    for x in elements:
        if x not in I:
            return True
    return False

def conditions(witness):
    try:
        elements, add, mul, zero, one, I = get_ring_ops(witness)
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = check_H1(elements, add, mul, zero, one)
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2(elements, add, mul, zero, I)
    except Exception:
        h2 = False
        
    try:
        h3 = check_H3(elements, add, mul, zero, one, I)
    except Exception:
        h3 = False
        
    try:
        neg_q = check_neg_Q(elements, I)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]
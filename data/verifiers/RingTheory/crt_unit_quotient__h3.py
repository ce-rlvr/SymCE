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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: The image of a in the quotient ring R/I is a unit",
    "¬Q: The ideal I and the principal ideal (a) are not comaximal in R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def get_elements(w):
    if isinstance(w, dict): return w.get('elements', [])
    return w.elements

def get_add(w):
    if isinstance(w, dict): return w['add']
    return w.add

def get_mul(w):
    if isinstance(w, dict): return w['mul']
    return w.mul

def get_zero(w):
    if isinstance(w, dict): return w['zero']
    return w.zero

def get_I(w):
    if isinstance(w, dict): return w['I']
    return w.I

def get_a(w):
    if isinstance(w, dict): return w['a']
    return w.a

def is_commutative_ring(w):
    elements = get_elements(w)
    add = get_add(w)
    mul = get_mul(w)
    zero = get_zero(w)
    
    if zero not in elements: return False
    
    for x in elements:
        if add(x, zero) != x or add(zero, x) != x: return False
        for y in elements:
            if add(x, y) not in elements: return False
            if add(x, y) != add(y, x): return False
            if mul(x, y) not in elements: return False
            if mul(x, y) != mul(y, x): return False
            for z in elements:
                if add(add(x, y), z) != add(x, add(y, z)): return False
                if mul(mul(x, y), z) != mul(x, mul(y, z)): return False
                if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): return False
    for x in elements:
        has_inv = False
        for y in elements:
            if add(x, y) == zero:
                has_inv = True
                break
        if not has_inv: return False
    return True

def is_ideal(w):
    elements = get_elements(w)
    add = get_add(w)
    mul = get_mul(w)
    zero = get_zero(w)
    I = get_I(w)
    
    if zero not in I: return False
    for x in I:
        if x not in elements: return False
        for y in I:
            if add(x, y) not in I: return False
        has_inv = False
        for y in I:
            if add(x, y) == zero:
                has_inv = True
                break
        if not has_inv: return False
        for r in elements:
            if mul(x, r) not in I: return False
    return True

def is_unit_in_quotient(w):
    elements = get_elements(w)
    add = get_add(w)
    mul = get_mul(w)
    zero = get_zero(w)
    I = get_I(w)
    a = get_a(w)
    
    if a not in elements: return False
    
    def sub(x, y):
        for inv in elements:
            if add(y, inv) == zero:
                return add(x, inv)
        return zero
        
    identities_mod_I = []
    for e in elements:
        is_id = True
        for r in elements:
            er = mul(e, r)
            diff = sub(er, r)
            if diff not in I:
                is_id = False
                break
        if is_id:
            identities_mod_I.append(e)
            
    if not identities_mod_I:
        return False
        
    for e in identities_mod_I:
        for b in elements:
            ab = mul(a, b)
            diff = sub(ab, e)
            if diff in I:
                return True
    return False

def is_comaximal(w):
    elements = get_elements(w)
    add = get_add(w)
    mul = get_mul(w)
    zero = get_zero(w)
    I = get_I(w)
    a = get_a(w)
    
    def sub(x, y):
        for inv in elements:
            if add(y, inv) == zero:
                return add(x, inv)
        return zero
        
    ideal_a = set([a, zero])
    changed = True
    while changed:
        changed = False
        new_elements = set()
        for x in ideal_a:
            for y in ideal_a:
                s = add(x, y)
                if s not in ideal_a:
                    new_elements.add(s)
                d = sub(x, y)
                if d not in ideal_a:
                    new_elements.add(d)
            for r in elements:
                p = mul(x, r)
                if p not in ideal_a:
                    new_elements.add(p)
        if new_elements:
            ideal_a.update(new_elements)
            changed = True
            
    I_plus_a = set()
    for i in I:
        for x in ideal_a:
            I_plus_a.add(add(i, x))
            
    for r in elements:
        if r not in I_plus_a:
            return False
    return True

def conditions(witness):
    try:
        h1 = is_commutative_ring(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ideal(witness)
    except Exception:
        h2 = False
        
    try:
        h3 = is_unit_in_quotient(witness)
    except Exception:
        h3 = False
        
    try:
        q = is_comaximal(witness)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]
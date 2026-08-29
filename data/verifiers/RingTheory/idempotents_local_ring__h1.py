import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import math
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

def get_elements(R):
    if hasattr(R, 'elements'):
        return list(R.elements)
    elif hasattr(R, 'ring_elements'):
        return list(R.ring_elements)
    else:
        return list(R)

def mul(R, x, y):
    if hasattr(R, 'mul'): return R.mul(x, y)
    return x * y

def add(R, x, y):
    if hasattr(R, 'add'): return R.add(x, y)
    return x + y

def zero(R):
    if hasattr(R, 'zero'): return R.zero
    elements = get_elements(R)
    for e in elements:
        if all(add(R, e, x) == x for x in elements):
            return e
    return None

def one(R):
    if hasattr(R, 'one'): return R.one
    elements = get_elements(R)
    for e in elements:
        if all(mul(R, e, x) == x and mul(R, x, e) == x for x in elements):
            return e
    return None

def closure(R, S, elements, z):
    ideal = []
    for x in S:
        if x not in ideal:
            ideal.append(x)
    if z not in ideal:
        ideal.append(z)
        
    to_process = list(ideal)
    
    while to_process:
        next_process = []
        current_ideal = list(ideal)
        
        for x in to_process:
            for y in current_ideal:
                s1 = add(R, x, y)
                if s1 not in ideal:
                    ideal.append(s1)
                    next_process.append(s1)
                s2 = add(R, y, x)
                if s2 not in ideal:
                    ideal.append(s2)
                    next_process.append(s2)
                    
        for x in to_process:
            for r in elements:
                m1 = mul(R, x, r)
                if m1 not in ideal:
                    ideal.append(m1)
                    next_process.append(m1)
                m2 = mul(R, r, x)
                if m2 not in ideal:
                    ideal.append(m2)
                    next_process.append(m2)
                    
        to_process = next_process
        
    return ideal

def ideals_equal(I1, I2):
    if len(I1) != len(I2): return False
    for x in I1:
        if x not in I2: return False
    return True

def is_in_ideals(I, ideals):
    for J in ideals:
        if ideals_equal(I, J): return True
    return False

def get_two_sided_ideals(R):
    elements = get_elements(R)
    z = zero(R)
    
    principal_ideals = []
    for x in elements:
        I = closure(R, [x], elements, z)
        if not is_in_ideals(I, principal_ideals):
            principal_ideals.append(I)
            
    ideals = list(principal_ideals)
    to_process = list(principal_ideals)
    
    while to_process:
        next_process = []
        current_ideals = list(ideals)
        
        for I1 in to_process:
            for I2 in current_ideals:
                sum_ideal = []
                for x in I1:
                    for y in I2:
                        s = add(R, x, y)
                        if s not in sum_ideal:
                            sum_ideal.append(s)
                if not is_in_ideals(sum_ideal, ideals):
                    ideals.append(sum_ideal)
                    next_process.append(sum_ideal)
                    
        to_process = next_process
        
    return ideals

def is_local_ring(R):
    elements = get_elements(R)
    z = zero(R)
    o = one(R)
    if z is None or o is None:
        return False
    if z == o:
        return False
        
    ideals = get_two_sided_ideals(R)
    
    proper_ideals = []
    for I in ideals:
        if len(I) < len(elements):
            proper_ideals.append(I)
            
    if not proper_ideals:
        return False
        
    maximal_ideals = []
    for I in proper_ideals:
        is_maximal = True
        for J in proper_ideals:
            if not ideals_equal(I, J):
                is_subset = True
                for x in I:
                    if x not in J:
                        is_subset = False
                        break
                if is_subset:
                    is_maximal = False
                    break
        if is_maximal:
            maximal_ideals.append(I)
            
    return len(maximal_ideals) == 1

def neg_Q(R):
    elements = get_elements(R)
    z = zero(R)
    o = one(R)
    for e in elements:
        if mul(R, e, e) == e:
            if e != z and e != o:
                return True
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = is_local_ring(witness)
    except Exception:
        h1 = False
        
    try:
        nq = neg_Q(witness)
    except Exception:
        nq = False
        
    return [h1, nq]

CONDITION_LABELS = [
    "H_1: R is a local ring",
    "¬Q: R has an idempotent element other than 0 and 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
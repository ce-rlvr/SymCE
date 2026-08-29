import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def make_op(op_data, elements):
    if callable(op_data):
        return op_data
    elif isinstance(op_data, (list, tuple)):
        def op(x, y):
            i = elements.index(x)
            j = elements.index(y)
            return op_data[i][j]
        return op
    elif isinstance(op_data, dict):
        def op(x, y):
            return op_data[(x, y)]
        return op
    else:
        raise ValueError("Unknown op format")

def extract_ring(witness):
    if isinstance(witness, dict):
        elements = list(witness['elements'])
        add_data = witness['add']
        mul_data = witness['mul']
        zero = witness['zero']
        P_elements = list(witness['P_elements'])
    elif isinstance(witness, (list, tuple)) and len(witness) == 5:
        elements = list(witness[0])
        add_data = witness[1]
        mul_data = witness[2]
        zero = witness[3]
        P_elements = list(witness[4])
    else:
        elements = list(witness.elements)
        add_data = witness.add
        mul_data = witness.mul
        zero = witness.zero
        P_elements = list(witness.P_elements)
        
    add = make_op(add_data, elements)
    mul = make_op(mul_data, elements)
    return elements, add, mul, zero, P_elements

def is_boolean_ring(elements, add, mul, zero):
    if zero not in elements: return False
    if len(elements) > 100: return False
    
    for x in elements:
        if mul(x, x) != x: return False
        for y in elements:
            try:
                if add(x, y) not in elements: return False
                if mul(x, y) not in elements: return False
            except Exception:
                return False
                
    for x in elements:
        for y in elements:
            if add(x, y) != add(y, x): return False
            
    for x in elements:
        for y in elements:
            for z in elements:
                if add(add(x, y), z) != add(x, add(y, z)): return False
                
    for x in elements:
        if add(x, zero) != x: return False
        if add(zero, x) != x: return False
        
    for x in elements:
        if add(x, x) != zero: return False
        
    for x in elements:
        for y in elements:
            for z in elements:
                if mul(mul(x, y), z) != mul(x, mul(y, z)): return False
                
    for x in elements:
        for y in elements:
            for z in elements:
                if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): return False
                if mul(add(x, y), z) != add(mul(x, z), mul(y, z)): return False
                
    return True

def get_identity(elements, mul):
    for e in elements:
        is_id = True
        for x in elements:
            if mul(e, x) != x or mul(x, e) != x:
                is_id = False
                break
        if is_id:
            return e
    return None

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, zero, P_elements = extract_ring(witness)
    except Exception:
        return [False, False, False]
        
    # H1: R is a Boolean ring
    try:
        h1 = is_boolean_ring(elements, add, mul, zero)
    except Exception:
        h1 = False
        
    # H2: P is the prime subring of R
    try:
        e = get_identity(elements, mul)
        if e is not None:
            if e == zero:
                expected_P = [zero]
            else:
                expected_P = [zero, e]
        else:
            expected_P = [zero]
            
        h2 = len(P_elements) == len(expected_P) and all(x in expected_P for x in P_elements)
    except Exception:
        h2 = False
        
    # neg_Q: P is NOT isomorphic to Z/2Z
    try:
        # P is isomorphic to Z/2Z iff it has exactly 2 elements.
        # Any 2-element subring of a Boolean ring is isomorphic to Z/2Z.
        neg_q = len(P_elements) != 2
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: P is the prime subring of R",
    "¬Q: P is not isomorphic to Z/2Z"
]

N_HYP = 2
NEG_Q_INDEX = 2
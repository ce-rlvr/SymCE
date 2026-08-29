import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

def get_add(R):
    if hasattr(R, 'add'):
        return R.add
    return lambda x, y: x + y

def get_mul(R):
    if hasattr(R, 'mul'):
        return R.mul
    return lambda x, y: x * y

def is_boolean_ring(R):
    try:
        elements = list(R.elements)
        zero = R.zero
        add = get_add(R)
        mul = get_mul(R)
        
        if zero not in elements:
            return False
            
        for x in elements:
            if add(x, zero) != x or add(zero, x) != x:
                return False
            if mul(x, x) != x:
                return False
                
            has_inv = False
            for y in elements:
                s = add(x, y)
                p = mul(x, y)
                
                if s not in elements or p not in elements:
                    return False
                    
                if s == zero and add(y, x) == zero:
                    has_inv = True
                    
                if s != add(y, x):
                    return False
                    
                for z in elements:
                    if add(s, z) != add(x, add(y, z)):
                        return False
                    if mul(p, z) != mul(x, mul(y, z)):
                        return False
                    if mul(x, add(y, z)) != add(p, mul(x, z)):
                        return False
                    if mul(s, z) != add(mul(x, z), mul(y, z)):
                        return False
                        
            if not has_inv:
                return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, x = witness
            check_all_x = False
        else:
            R = witness
            check_all_x = True
    except Exception:
        return [False, False]
        
    h1 = is_boolean_ring(R)
    
    neg_q = False
    try:
        add = get_add(R)
        if check_all_x:
            for elem in R.elements:
                if add(elem, elem) != R.zero:
                    neg_q = True
                    break
        else:
            if all(x != e for e in R.elements):
                neg_q = False
            elif add(x, x) != R.zero:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: x + x != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def eq(x, y):
    try:
        return bool(x == y)
    except Exception:
        return False

def contains(lst, x):
    return any(eq(e, x) for e in lst)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            elements = list(witness.get('elements', []))
            add = witness.get('add', lambda a, b: a + b)
            mul = witness.get('mul', lambda a, b: a * b)
            zero = witness.get('zero', None)
            le = witness.get('le', lambda a, b: a <= b)
        elif hasattr(witness, 'elements'):
            elements = list(witness.elements)
            add = getattr(witness, 'add', lambda a, b: a + b)
            mul = getattr(witness, 'mul', lambda a, b: a * b)
            zero = getattr(witness, 'zero', None)
            le = getattr(witness, 'le', lambda a, b: a <= b)
        else:
            elements = list(witness)
            add = lambda a, b: a + b
            mul = lambda a, b: a * b
            zero = None
            le = lambda a, b: a <= b
            
        if not elements or len(elements) > 50:
            return [False, False]
            
        if zero is None:
            for e in elements:
                try:
                    if all(eq(add(e, x), x) and eq(add(x, e), x) for x in elements):
                        zero = e
                        break
                except Exception:
                    pass
                    
        if zero is None:
            return [False, False]
            
    except Exception:
        return [False, False]

    # H_1: R is a Boolean ring
    h1 = False
    try:
        is_ring = True
        for a in elements:
            if not eq(add(a, zero), a) or not eq(add(zero, a), a):
                is_ring = False
                break
            
            has_inv = False
            for b in elements:
                if eq(add(a, b), zero) and eq(add(b, a), zero):
                    has_inv = True
                    break
            if not has_inv:
                is_ring = False
                break
                
            if not eq(mul(a, a), a):
                is_ring = False
                break
                
            for b in elements:
                if not contains(elements, add(a, b)): 
                    is_ring = False
                    break
                if not contains(elements, mul(a, b)): 
                    is_ring = False
                    break
                if not eq(add(a, b), add(b, a)): 
                    is_ring = False
                    break
                
                for c in elements:
                    if not eq(add(add(a, b), c), add(a, add(b, c))): 
                        is_ring = False
                        break
                    if not eq(mul(mul(a, b), c), mul(a, mul(b, c))): 
                        is_ring = False
                        break
                    if not eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))): 
                        is_ring = False
                        break
                    if not eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))): 
                        is_ring = False
                        break
                if not is_ring: 
                    break
            if not is_ring: 
                break
        h1 = is_ring
    except Exception:
        h1 = False

    # neg_Q: The relation <= is NOT a partial order on R
    neg_q = False
    try:
        is_po = True
        for a in elements:
            if not bool(le(a, a)):
                is_po = False
                break
            for b in elements:
                if bool(le(a, b)) and bool(le(b, a)) and not eq(a, b):
                    is_po = False
                    break
                for c in elements:
                    if bool(le(a, b)) and bool(le(b, c)) and not bool(le(a, c)):
                        is_po = False
                        break
                if not is_po: 
                    break
            if not is_po: 
                break
        neg_q = not is_po
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: The relation <= is not a partial order on R"
]

N_HYP = 1
NEG_Q_INDEX = 1
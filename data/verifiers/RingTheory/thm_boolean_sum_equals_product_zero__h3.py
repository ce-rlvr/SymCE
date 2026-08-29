import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

class CustomRing:
    def __init__(self, elements, add, mul, zero):
        self.elements = elements
        self.add = add
        self.mul = mul
        self.zero = zero

Z2 = CustomRing([0, 1], lambda a, b: (a + b) % 2, lambda a, b: (a * b) % 2, 0)
Z2xZ2 = CustomRing(
    [(0,0), (0,1), (1,0), (1,1)],
    lambda a, b: ((a[0]+b[0])%2, (a[1]+b[1])%2),
    lambda a, b: ((a[0]*b[0])%2, (a[1]*b[1])%2),
    (0,0)
)

def get_func(op):
    if isinstance(op, dict):
        return lambda a, b: op.get((a, b), None)
    return op

def extract_ring(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            R, x, y = witness
            if isinstance(R, int):
                n = R
                elements = list(range(n))
                add = lambda a, b: (a + b) % n
                mul = lambda a, b: (a * b) % n
                zero = 0
                return elements, add, mul, zero, x, y
            elif hasattr(R, 'elements') and hasattr(R, 'add') and hasattr(R, 'mul') and hasattr(R, 'zero'):
                return list(R.elements), get_func(R.add), get_func(R.mul), R.zero, x, y
        elif len(witness) == 6:
            elements, add, mul, zero, x, y = witness
            return list(elements), get_func(add), get_func(mul), zero, x, y
    raise ValueError("Cannot extract ring from witness")

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul, zero, x, y = extract_ring(witness)
        if len(elements) > 100:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    # H_1: R is a Boolean ring
    h1 = False
    try:
        if zero not in elements:
            is_ring = False
        else:
            is_ring = True
            
        if is_ring:
            is_ring = all(add(a, b) in elements and mul(a, b) in elements for a in elements for b in elements)
            
        if is_ring:
            is_ring = all(add(a, zero) == a and add(zero, a) == a for a in elements)
            
        if is_ring:
            is_ring = all(add(a, b) == add(b, a) for a in elements for b in elements)
            
        if is_ring:
            is_ring = all(add(a, add(b, c)) == add(add(a, b), c) for a in elements for b in elements for c in elements)
            
        if is_ring:
            is_ring = all(any(add(a, b) == zero and add(b, a) == zero for b in elements) for a in elements)
            
        if is_ring:
            is_ring = all(mul(a, mul(b, c)) == mul(mul(a, b), c) for a in elements for b in elements for c in elements)
            
        if is_ring:
            is_ring = all(mul(a, add(b, c)) == add(mul(a, b), mul(a, c)) and mul(add(a, b), c) == add(mul(a, c), mul(b, c)) for a in elements for b in elements for c in elements)
            
        if is_ring:
            is_ring = all(mul(a, a) == a for a in elements)
            
        h1 = bool(is_ring)
    except Exception:
        h1 = False

    # H_2: x and y are elements of R
    h2 = False
    try:
        h2 = bool((x in elements) and (y in elements))
    except Exception:
        h2 = False

    # neg_Q: not (x = 0 and y = 0)
    neg_q = False
    try:
        neg_q = bool((x != zero) or (y != zero))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: x and y are elements of R",
    "¬Q: x != 0 or y != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2
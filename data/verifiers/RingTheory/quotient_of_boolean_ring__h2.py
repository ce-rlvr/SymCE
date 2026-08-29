import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup for standard rings
class FiniteRing:
    def __init__(self, elements, add, mul):
        self.elements = elements
        self.add = add
        self.mul = mul

Z2_elements = [0, 1]
Z2_add = lambda x, y: (x + y) % 2
Z2_mul = lambda x, y: (x * y) % 2
Z2 = FiniteRing(Z2_elements, Z2_add, Z2_mul)

Z2xZ2_elements = [(0,0), (0,1), (1,0), (1,1)]
Z2xZ2_add = lambda x, y: ((x[0]+y[0])%2, (x[1]+y[1])%2)
Z2xZ2_mul = lambda x, y: ((x[0]*y[0])%2, (x[1]*y[1])%2)
Z2xZ2 = FiniteRing(Z2xZ2_elements, Z2xZ2_add, Z2xZ2_mul)

def get_op(op, elements):
    if isinstance(op, dict):
        return lambda a, b: op[(a, b)]
    elif callable(op):
        return op
    elif isinstance(op, list):
        idx = {e: i for i, e in enumerate(elements)}
        return lambda a, b: op[idx[a]][idx[b]]
    else:
        raise ValueError("Unknown operation format")

def parse_witness(witness):
    if hasattr(witness, 'R') and hasattr(witness, 'I'):
        R = witness.R
        I = witness.I
    elif isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
    elif isinstance(witness, tuple) and len(witness) == 4:
        elements, add_op, mul_op, I = witness
        add = get_op(add_op, elements)
        mul = get_op(mul_op, elements)
        return elements, add, mul, I
    else:
        raise ValueError("Unknown witness format")

    if hasattr(R, 'elements') and hasattr(R, 'add') and hasattr(R, 'mul'):
        elements = R.elements
        add = R.add
        mul = R.mul
    elif isinstance(R, tuple) and len(R) == 3:
        elements, add_op, mul_op = R
        add = get_op(add_op, elements)
        mul = get_op(mul_op, elements)
    else:
        raise ValueError("Unknown R format")
        
    return elements, add, mul, I

def check_boolean_ring(elements, add, mul):
    elements = list(elements)
    n = len(elements)
    if n == 0: return False
    
    # Check closure
    for a in elements:
        for b in elements:
            if add(a, b) not in elements: return False
            if mul(a, b) not in elements: return False

    # Check add commutativity and associativity
    for a in elements:
        for b in elements:
            if add(a, b) != add(b, a): return False
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False

    # Find zero
    zeros_list = []
    for z in elements:
        if all(add(z, a) == a for a in elements):
            zeros_list.append(z)
    if len(zeros_list) != 1: return False
    zero = zeros_list[0]

    # Check additive inverses
    for a in elements:
        if not any(add(a, b) == zero for b in elements): return False

    # Check mul associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False

    # Check distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False

    # Check Boolean property (x^2 = x)
    for a in elements:
        if mul(a, a) != a: return False

    return True

def check_ideal(elements, add, mul, I):
    elements = list(elements)
    I = list(I)
    if not all(x in elements for x in I): return False
    if len(I) == 0: return False

    zeros_list = [z for z in elements if all(add(z, a) == a for a in elements)]
    if not zeros_list: return False
    zero = zeros_list[0]

    # Check additive subgroup
    if zero not in I: return False
    for i in I:
        for j in I:
            if add(i, j) not in I: return False

    for i in I:
        if not any(add(i, j) == zero for j in I): return False

    # Check ideal absorption property
    for i in I:
        for r in elements:
            if mul(i, r) not in I: return False
            if mul(r, i) not in I: return False

    return True

def conditions(witness):
    try:
        elements, add, mul, I = parse_witness(witness)
    except Exception:
        return [False, False]

    try:
        h1 = check_boolean_ring(elements, add, mul)
    except Exception:
        h1 = False

    try:
        # The quotient ring R/I is a well-defined ring (and thus a Boolean ring) 
        # if and only if I is an ideal of R.
        q = check_ideal(elements, add, mul, I)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: The quotient ring R/I is not a well-defined Boolean ring"
]

N_HYP = 1
NEG_Q_INDEX = 1
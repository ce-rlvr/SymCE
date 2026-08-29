import math
import itertools
import functools
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def eval_op(op, x, y):
    if callable(op):
        return op(x, y)
    try:
        return op[x][y]
    except Exception:
        return op[(x, y)]

def is_boolean_ring(elements, add, mul):
    elements = list(elements)
    n = len(elements)
    if n == 0: 
        return False
    
    zero = None
    for e in elements:
        if all(eval_op(add, e, x) == x and eval_op(add, x, e) == x for x in elements):
            zero = e
            break
    if zero is None: 
        return False
    
    for x in elements:
        if not any(eval_op(add, x, y) == zero and eval_op(add, y, x) == zero for y in elements):
            return False
        if eval_op(mul, x, x) != x:
            return False
        for y in elements:
            if eval_op(add, x, y) not in elements: 
                return False
            if eval_op(mul, x, y) not in elements: 
                return False
            if eval_op(add, x, y) != eval_op(add, y, x): 
                return False
            for z in elements:
                if eval_op(add, eval_op(add, x, y), z) != eval_op(add, x, eval_op(add, y, z)): 
                    return False
                if eval_op(mul, eval_op(mul, x, y), z) != eval_op(mul, x, eval_op(mul, y, z)): 
                    return False
                if eval_op(mul, x, eval_op(add, y, z)) != eval_op(add, eval_op(mul, x, y), eval_op(mul, x, z)): 
                    return False
                if eval_op(mul, eval_op(add, x, y), z) != eval_op(add, eval_op(mul, x, z), eval_op(mul, y, z)): 
                    return False
    return True

def is_join_valid(elements, join):
    elements = list(elements)
    for x in elements:
        if eval_op(join, x, x) != x:
            return False
        for y in elements:
            if eval_op(join, x, y) not in elements:
                return False
            if eval_op(join, x, y) != eval_op(join, y, x):
                return False
            for z in elements:
                if eval_op(join, eval_op(join, x, y), z) != eval_op(join, x, eval_op(join, y, z)):
                    return False
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            elements, add, mul, join = witness
        elif hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'join'):
            elements = witness.elements
            add = witness.add
            mul = witness.mul
            join = witness.join
        else:
            elements = list(witness)
            add = lambda x, y: x + y
            mul = lambda x, y: x * y
            join = lambda x, y: x | y
    except Exception:
        return [False, False]
        
    try:
        h1 = is_boolean_ring(elements, add, mul)
    except Exception:
        h1 = False
        
    try:
        q = is_join_valid(elements, join)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: The operation ∨ is not associative, commutative, and idempotent on R"
]

N_HYP = 1
NEG_Q_INDEX = 1
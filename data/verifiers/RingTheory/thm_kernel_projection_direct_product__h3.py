import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_field(witness, field):
    if isinstance(witness, dict):
        return witness[field]
    else:
        return getattr(witness, field)

def evaluate(op, a, b):
    if isinstance(op, dict):
        return op[(a, b)]
    return op(a, b)

def evaluate1(op, arg):
    if isinstance(op, dict):
        return op[arg]
    try:
        return op(arg)
    except TypeError:
        if isinstance(arg, tuple):
            return op(*arg)
        raise

def check_ring(R, add, mul, zero):
    R_list = list(R)
    if len(R_list) > 100:
        return False
    R_set = set(R_list)
    if zero not in R_set: 
        return False
    for a in R_list:
        for b in R_list:
            if evaluate(add, a, b) not in R_set: return False
            if evaluate(mul, a, b) not in R_set: return False
    for a in R_list:
        for b in R_list:
            for c in R_list:
                if evaluate(add, evaluate(add, a, b), c) != evaluate(add, a, evaluate(add, b, c)): return False
                if evaluate(mul, evaluate(mul, a, b), c) != evaluate(mul, a, evaluate(mul, b, c)): return False
    for a in R_list:
        for b in R_list:
            if evaluate(add, a, b) != evaluate(add, b, a): return False
    for a in R_list:
        if evaluate(add, a, zero) != a: return False
        if evaluate(add, zero, a) != a: return False
    for a in R_list:
        has_inv = False
        for b in R_list:
            if evaluate(add, a, b) == zero and evaluate(add, b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
    for a in R_list:
        for b in R_list:
            for c in R_list:
                if evaluate(mul, a, evaluate(add, b, c)) != evaluate(add, evaluate(mul, a, b), evaluate(mul, a, c)): return False
                if evaluate(mul, evaluate(add, a, b), c) != evaluate(add, evaluate(mul, a, c), evaluate(mul, b, c)): return False
    return True

def conditions(witness):
    try:
        R1 = get_field(witness, 'R1')
        add1 = get_field(witness, 'add1')
        mul1 = get_field(witness, 'mul1')
        zero1 = get_field(witness, 'zero1')
        
        R2 = get_field(witness, 'R2')
        add2 = get_field(witness, 'add2')
        mul2 = get_field(witness, 'mul2')
        zero2 = get_field(witness, 'zero2')
        
        pi_1 = get_field(witness, 'pi_1')
    except Exception:
        return [False, False, False]

    # H1: R_1 and R_2 are rings
    try:
        h1 = check_ring(R1, add1, mul1, zero1) and check_ring(R2, add2, mul2, zero2)
    except Exception:
        h1 = False

    # H2: R_1 x R_2 is the direct product ring
    try:
        h2 = True
        R1_list = list(R1)
        R2_list = list(R2)
        for x in R1_list:
            for y in R2_list:
                val = evaluate1(pi_1, (x, y))
                if val not in R1_list:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # neg_Q: The kernel of pi_1 is NOT the ideal {(0, y) | y in R_2}
    try:
        expected_kernel = set()
        for y in list(R2):
            expected_kernel.add((zero1, y))
            
        actual_kernel = set()
        for x in list(R1):
            for y in list(R2):
                if evaluate1(pi_1, (x, y)) == zero1:
                    actual_kernel.add((x, y))
                    
        neg_q = actual_kernel != expected_kernel
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R_1 and R_2 are rings",
    "H_2: R_1 x R_2 is the direct product ring",
    "¬Q: The kernel of pi_1 is not the ideal {(0, y) | y in R_2}"
]

N_HYP = 2
NEG_Q_INDEX = 2
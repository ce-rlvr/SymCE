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

def parse_ring(R):
    if isinstance(R, int) and R > 0:
        elements = list(range(R))
        add = lambda a, b, mod=R: (a + b) % mod
        mul = lambda a, b, mod=R: (a * b) % mod
        zero = 0
        return elements, add, mul, zero
    elif isinstance(R, tuple) and len(R) == 3:
        elements, add_op, mul_op = R
        add = lambda a, b: add_op(a, b) if callable(add_op) else add_op[(a, b)]
        mul = lambda a, b: mul_op(a, b) if callable(mul_op) else mul_op[(a, b)]
        zero = None
        for e in elements:
            if all(add(e, a) == a for a in elements):
                zero = e
                break
        return elements, add, mul, zero
    elif isinstance(R, list):
        elements = R
        add = lambda a, b: a + b
        mul = lambda a, b: a * b
        zero = None
        for e in elements:
            if all(add(e, a) == a for a in elements):
                zero = e
                break
        return elements, add, mul, zero
    return None

def is_ring(parsed_R):
    if parsed_R is None: return False
    elements, add, mul, zero = parsed_R
    if zero is None: return False
    if not elements: return False
    if len(elements) > 50: return False
    try:
        # Check closure
        for a in elements:
            for b in elements:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
        # Check add associativity
        for a in elements:
            for b in elements:
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
        # Check add commutativity
        for a in elements:
            for b in elements:
                if add(a, b) != add(b, a): return False
        # Check add inverse
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
        return True
    except Exception:
        return False

def is_nilpotent(x, parsed_R):
    elements, add, mul, zero = parsed_R
    if x not in elements: return False
    curr = x
    for _ in range(len(elements)):
        if curr == zero: return True
        curr = mul(curr, x)
    return False

def apply_f(f, x):
    if callable(f): return f(x)
    elif isinstance(f, (dict, list, tuple)): return f[x]
    else: return None

def conditions(witness):
    """
    witness is expected to be a tuple: (R, S, f, x)
    where R and S are rings (can be integers n for Z_n),
    f is a function/dict/list mapping elements of R to S,
    and x is an element of R.
    """
    try:
        if len(witness) != 4:
            return [False, False, False]
        R, S, f, x = witness
    except Exception:
        return [False, False, False]
    
    try:
        parsed_R = parse_ring(R)
        parsed_S = parse_ring(S)
        h1 = is_ring(parsed_R) and is_ring(parsed_S)
    except Exception:
        h1 = False

    try:
        h2 = is_ring(parsed_R) and is_nilpotent(x, parsed_R)
    except Exception:
        h2 = False

    try:
        if not is_ring(parsed_S):
            neg_q = False
        else:
            fx = apply_f(f, x)
            elements_S = parsed_S[0]
            if fx not in elements_S:
                neg_q = True
            else:
                neg_q = not is_nilpotent(fx, parsed_S)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: x is a nilpotent element in R",
    "¬Q: The image f(x) is not a nilpotent element in S"
]

N_HYP = 2
NEG_Q_INDEX = 2
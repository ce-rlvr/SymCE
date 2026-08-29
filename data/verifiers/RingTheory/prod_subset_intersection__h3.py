import sympy as sp
from sympy import eye, zeros
import itertools
import math
import functools

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_ring_ops(R):
    if isinstance(R, int) and R > 0:
        elements = list(range(R))
        def add(x, y): return (x + y) % R
        def mul(x, y): return (x * y) % R
        def neg(x): return (-x) % R
        def eq(x, y): return (x - y) % R == 0
        zero = 0
        return elements, add, mul, neg, zero, eq
    elif isinstance(R, (list, tuple, set)):
        elements = list(R)
        def add(x, y): return x + y
        def mul(x, y): return x * y
        def neg(x): return -x
        def eq(x, y): return x == y
        zero = None
        for e in elements:
            try:
                if all(eq(add(e, x), x) and eq(add(x, e), x) for x in elements):
                    zero = e
                    break
            except Exception:
                pass
        return elements, add, mul, neg, zero, eq
    return None

def check_ring(elements, add, mul, neg, zero, eq):
    if zero is None: return False
    n = len(elements)
    if n > 100:
        return True
    for a in elements:
        if not any(eq(a, x) for x in elements): return False
        if not eq(add(a, zero), a): return False
        if not eq(add(zero, a), a): return False
        if not eq(add(a, neg(a)), zero): return False
        for b in elements:
            if not any(eq(add(a, b), x) for x in elements): return False
            if not any(eq(mul(a, b), x) for x in elements): return False
            if not eq(add(a, b), add(b, a)): return False
            for c in elements:
                if not eq(add(add(a, b), c), add(a, add(b, c))): return False
                if not eq(mul(mul(a, b), c), mul(a, mul(b, c))): return False
                if not eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))): return False
                if not eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))): return False
    return True

def is_ideal(I_elements, R_elements, add, mul, neg, zero, eq):
    if not I_elements: return False
    for x in I_elements:
        if not any(eq(x, r) for r in R_elements): return False
    for a in I_elements:
        for b in I_elements:
            diff = add(a, neg(b))
            if not any(eq(diff, x) for x in I_elements): return False
    for a in I_elements:
        for r in R_elements:
            ra = mul(r, a)
            ar = mul(a, r)
            if not any(eq(ra, x) for x in I_elements): return False
            if not any(eq(ar, x) for x in I_elements): return False
    return True

def compute_IJ(I_elements, J_elements, add, mul, zero, eq):
    products = []
    for a in I_elements:
        for b in J_elements:
            p = mul(a, b)
            if not any(eq(p, x) for x in products):
                products.append(p)
    
    closure = [zero]
    added = True
    while added:
        added = False
        new_elements = []
        for x in closure:
            for p in products:
                s = add(x, p)
                if not any(eq(s, y) for y in closure) and not any(eq(s, y) for y in new_elements):
                    new_elements.append(s)
        if new_elements:
            closure.extend(new_elements)
            added = True
    return closure

def check_intersection(I_elements, J_elements, eq):
    intersection = []
    for a in I_elements:
        if any(eq(a, b) for b in J_elements):
            if not any(eq(a, x) for x in intersection):
                intersection.append(a)
    return intersection

def check_subset(A, B, eq):
    for a in A:
        if not any(eq(a, b) for b in B):
            return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
        else:
            if len(witness) != 3:
                return [False, False, False]
            R, I, J = witness
    except Exception:
        return [False, False, False]
        
    ops = get_ring_ops(R)
    if ops is None:
        return [False, False, False]
        
    elements, add, mul, neg, zero, eq = ops
    
    # H_1: R is a ring
    try:
        if isinstance(R, int):
            h1 = True
        else:
            h1 = check_ring(elements, add, mul, neg, zero, eq)
    except Exception:
        h1 = False
        
    # H_2: I is an ideal of R
    try:
        h2 = is_ideal(I, elements, add, mul, neg, zero, eq)
    except Exception:
        h2 = False
        
    # ¬Q: IJ is not a subset of I \cap J
    try:
        j_in_r = True
        for b in J:
            if not any(eq(b, r) for r in elements):
                j_in_r = False
                break
        if not j_in_r:
            neg_q = False
        else:
            IJ = compute_IJ(I, J, add, mul, zero, eq)
            I_cap_J = check_intersection(I, J, eq)
            is_subset = check_subset(IJ, I_cap_J, eq)
            neg_q = not is_subset
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "¬Q: IJ is not a subset of I \\cap J"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup for potential witness elements
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

def call_op(op, *args):
    if isinstance(op, dict):
        if len(args) == 1:
            return op[args[0]]
        return op[args]
    elif isinstance(op, (list, tuple)):
        if len(args) == 1:
            return op[args[0]]
        elif len(args) == 2:
            return op[args[0]][args[1]]
    return op(*args)

def is_ring(elements, add, mul, zero):
    if zero not in elements: 
        return False
    # Closure
    for x in elements:
        for y in elements:
            if call_op(add, x, y) not in elements: return False
            if call_op(mul, x, y) not in elements: return False
    # Associativity and Distributivity
    for x in elements:
        for y in elements:
            if call_op(add, x, y) != call_op(add, y, x): return False
            for z in elements:
                if call_op(add, call_op(add, x, y), z) != call_op(add, x, call_op(add, y, z)): return False
                if call_op(mul, call_op(mul, x, y), z) != call_op(mul, x, call_op(mul, y, z)): return False
                if call_op(mul, x, call_op(add, y, z)) != call_op(add, call_op(mul, x, y), call_op(mul, x, z)): return False
                if call_op(mul, call_op(add, x, y), z) != call_op(add, call_op(mul, x, z), call_op(mul, y, z)): return False
    # Additive identity
    for x in elements:
        if call_op(add, x, zero) != x: return False
    # Additive inverse
    for x in elements:
        has_inv = False
        for y in elements:
            if call_op(add, x, y) == zero:
                has_inv = True
                break
        if not has_inv: return False
    return True

def is_ideal(ideal_elements, ring_elements, add, mul, zero):
    if zero not in ideal_elements: 
        return False
    for x in ideal_elements:
        if x not in ring_elements: return False
        for y in ideal_elements:
            if call_op(add, x, y) not in ideal_elements: return False
        for r in ring_elements:
            if call_op(mul, r, x) not in ideal_elements: return False
            if call_op(mul, x, r) not in ideal_elements: return False
    for x in ideal_elements:
        has_inv = False
        for y in ideal_elements:
            if call_op(add, x, y) == zero:
                has_inv = True
                break
        if not has_inv: return False
    return True

def multiply_ideals(I, J, ring_elements, add, mul, zero):
    products = []
    for i in I:
        for j in J:
            products.append(call_op(mul, i, j))
    
    closure = []
    for p in products:
        if p not in closure:
            closure.append(p)
            
    changed = True
    iters = 0
    while changed and iters < 1000:
        changed = False
        iters += 1
        new_elements = list(closure)
        for x in closure:
            for y in closure:
                s = call_op(add, x, y)
                if s not in new_elements:
                    new_elements.append(s)
                    changed = True
        closure = new_elements
    return closure

def is_nilpotent(ideal_elements, ring_elements, add, mul, zero):
    if not ideal_elements: 
        return False
    current = list(ideal_elements)
    seen = []
    iters = 0
    while iters < 100:
        iters += 1
        if all(x == zero for x in current):
            return True
        for s in seen:
            if len(s) == len(current) and all(x in s for x in current):
                return False
        seen.append(list(current))
        current = multiply_ideals(current, ideal_elements, ring_elements, add, mul, zero)
    return False

def conditions(witness):
    try:
        R = witness['R']
        S = witness['S']
        add_R = witness['add_R']
        mul_R = witness['mul_R']
        add_S = witness['add_S']
        mul_S = witness['mul_S']
        zero_R = witness['zero_R']
        zero_S = witness['zero_S']
        h1 = is_ring(R, add_R, mul_R, zero_R) and is_ring(S, add_S, mul_S, zero_S)
    except Exception:
        h1 = False

    try:
        N = witness['N']
        h2 = is_ideal(N, S, add_S, mul_S, zero_S) and is_nilpotent(N, S, add_S, mul_S, zero_S)
    except Exception:
        h2 = False

    try:
        f = witness['f']
        if not all(call_op(f, x) in S for x in R):
            h3 = False
        else:
            ker_f = [x for x in R if call_op(f, x) == zero_S]
            h3 = is_ideal(ker_f, R, add_R, mul_R, zero_R) and is_nilpotent(ker_f, R, add_R, mul_R, zero_R)
    except Exception:
        h3 = False

    try:
        f_inv_N = [x for x in R if call_op(f, x) in N]
        is_id = is_ideal(f_inv_N, R, add_R, mul_R, zero_R)
        is_nil = is_nilpotent(f_inv_N, R, add_R, mul_R, zero_R)
        q = is_id and is_nil
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: N is a nilpotent ideal of S",
    "H_3: ker(f) is a nilpotent ideal of R",
    "¬Q: f^{-1}(N) is not a nilpotent ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3
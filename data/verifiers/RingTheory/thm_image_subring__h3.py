import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup
class Ring:
    def __init__(self, elements, add, mul):
        self.elements = list(elements)
        self.add = add
        self.mul = mul

Z2 = Ring([0, 1], lambda a, b: (a + b) % 2, lambda a, b: (a * b) % 2)
Z3 = Ring([0, 1, 2], lambda a, b: (a + b) % 3, lambda a, b: (a * b) % 3)
Z4 = Ring([0, 1, 2, 3], lambda a, b: (a + b) % 4, lambda a, b: (a * b) % 4)
Z6 = Ring([0, 1, 2, 3, 4, 5], lambda a, b: (a + b) % 6, lambda a, b: (a * b) % 6)

def call_op(op, a, b):
    if callable(op):
        return op(a, b)
    elif isinstance(op, dict):
        return op[(a, b)]
    else:
        try:
            return op[a][b]
        except Exception:
            return op[(a, b)]

def call_f(f, a):
    if callable(f):
        return f(a)
    elif isinstance(f, dict):
        return f[a]
    else:
        return f[a]

def is_ring(elements, add, mul):
    elements = list(elements)
    if not elements: return False
    
    # closure
    for a in elements:
        for b in elements:
            if call_op(add, a, b) not in elements: return False
            if call_op(mul, a, b) not in elements: return False
                
    # add commutativity
    for a in elements:
        for b in elements:
            if call_op(add, a, b) != call_op(add, b, a): return False
            
    # add associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if call_op(add, call_op(add, a, b), c) != call_op(add, a, call_op(add, b, c)): return False
                
    # zero
    zeros_list = [z for z in elements if all(call_op(add, z, a) == a for a in elements)]
    if len(zeros_list) != 1: return False
    zero = zeros_list[0]
    
    # add inverses
    for a in elements:
        if not any(call_op(add, a, b) == zero for b in elements): return False
        
    # mul associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if call_op(mul, call_op(mul, a, b), c) != call_op(mul, a, call_op(mul, b, c)): return False
                
    # distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if call_op(mul, a, call_op(add, b, c)) != call_op(add, call_op(mul, a, b), call_op(mul, a, c)): return False
                if call_op(mul, call_op(add, a, b), c) != call_op(add, call_op(mul, a, c), call_op(mul, b, c)): return False
                
    # identity
    ones = [e for e in elements if all(call_op(mul, e, a) == a and call_op(mul, a, e) == a for a in elements)]
    if len(ones) != 1: return False
    
    return True

def is_subring(elements, subset, add, mul):
    subset = list(subset)
    if not subset: return False
    for a in subset:
        if a not in elements: return False
    if not is_ring(subset, add, mul): return False
    
    ones_parent = [e for e in elements if all(call_op(mul, e, a) == a and call_op(mul, a, e) == a for a in elements)]
    ones_sub = [e for e in subset if all(call_op(mul, e, a) == a and call_op(mul, a, e) == a for a in subset)]
    if not ones_parent or not ones_sub: return False
    if ones_parent[0] != ones_sub[0]: return False
    
    return True

def parse_witness(witness):
    if len(witness) == 4:
        R, S, f, A = witness
        return R.elements, R.add, R.mul, S.elements, S.add, S.mul, f, A
    elif len(witness) == 8:
        return witness
    else:
        raise ValueError("Witness must have 4 or 8 elements")

def conditions(witness) -> list[bool]:
    try:
        R_elements, add_R, mul_R, S_elements, add_S, mul_S, f, A = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    # H1: R and S are rings
    try:
        h1_ok = is_ring(R_elements, add_R, mul_R) and is_ring(S_elements, add_S, mul_S)
    except Exception:
        h1_ok = False
        
    # H2: f is a ring homomorphism from R to S
    try:
        h2_ok = True
        for a in R_elements:
            if call_f(f, a) not in S_elements:
                h2_ok = False
                break
        if h2_ok:
            for a in R_elements:
                for b in R_elements:
                    if call_f(f, call_op(add_R, a, b)) != call_op(add_S, call_f(f, a), call_f(f, b)):
                        h2_ok = False
                    if call_f(f, call_op(mul_R, a, b)) != call_op(mul_S, call_f(f, a), call_f(f, b)):
                        h2_ok = False
        if h2_ok:
            ones_R = [e for e in R_elements if all(call_op(mul_R, e, x) == x and call_op(mul_R, x, e) == x for x in R_elements)]
            ones_S = [e for e in S_elements if all(call_op(mul_S, e, x) == x and call_op(mul_S, x, e) == x for x in S_elements)]
            if not ones_R or not ones_S:
                h2_ok = False
            elif call_f(f, ones_R[0]) != ones_S[0]:
                h2_ok = False
    except Exception:
        h2_ok = False
        
    # neg_Q: The image f(A) is NOT a subring of S
    try:
        subset_ok = True
        for a in A:
            if a not in R_elements:
                subset_ok = False
                break
        if not subset_ok:
            neg_q_ok = False
        else:
            f_A = []
            for a in A:
                val = call_f(f, a)
                if val not in f_A:
                    f_A.append(val)
            neg_q_ok = not is_subring(S_elements, f_A, add_S, mul_S)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a ring homomorphism from R to S",
    "¬Q: The image f(A) is not a subring of S"
]

N_HYP = 2
NEG_Q_INDEX = 2
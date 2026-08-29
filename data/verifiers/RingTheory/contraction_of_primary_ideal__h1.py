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

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: Q is a P-primary ideal of S",
    "¬Q: f^{-1}(Q) is not an f^{-1}(P)-primary ideal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def unique_elements(lst):
    res = []
    for x in lst:
        if x not in res:
            res.append(x)
    return res

def get_attr(obj, name):
    if isinstance(obj, dict):
        return obj[name]
    return getattr(obj, name)

def apply_op(op, a, b=None):
    if b is None:
        if isinstance(op, dict):
            return op[a]
        return op(a)
    else:
        if isinstance(op, dict):
            return op[(a, b)]
        return op(a, b)

def check_ring(elements, add, mul):
    if not elements: return False, None
    # check closure
    for a in elements:
        for b in elements:
            if apply_op(add, a, b) not in elements: return False, None
            if apply_op(mul, a, b) not in elements: return False, None
    
    # check add commutativity and associativity
    for a in elements:
        for b in elements:
            if apply_op(add, a, b) != apply_op(add, b, a): return False, None
            for c in elements:
                if apply_op(add, apply_op(add, a, b), c) != apply_op(add, a, apply_op(add, b, c)): return False, None
                
    # find zero
    zeros_list = []
    for z in elements:
        if all(apply_op(add, z, a) == a for a in elements):
            zeros_list.append(z)
    if len(zeros_list) != 1: return False, None
    zero = zeros_list[0]
    
    # check additive inverses
    for a in elements:
        if not any(apply_op(add, a, b) == zero for b in elements): return False, None
        
    # check mul associativity and commutativity
    for a in elements:
        for b in elements:
            if apply_op(mul, a, b) != apply_op(mul, b, a): return False, None
            for c in elements:
                if apply_op(mul, apply_op(mul, a, b), c) != apply_op(mul, a, apply_op(mul, b, c)): return False, None
                
    # check distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if apply_op(mul, a, apply_op(add, b, c)) != apply_op(add, apply_op(mul, a, b), apply_op(mul, a, c)): return False, None
                
    return True, zero

def check_ideal(elements, add, mul, zero, I):
    if not I: return False
    if not all(x in elements for x in I): return False
    # closed under add
    for a in I:
        for b in I:
            if apply_op(add, a, b) not in I: return False
    # closed under mul by elements
    for r in elements:
        for x in I:
            if apply_op(mul, r, x) not in I: return False
    # closed under additive inverse
    for x in I:
        inv_found = False
        for y in I:
            if apply_op(add, x, y) == zero:
                inv_found = True
                break
        if not inv_found: return False
    return True

def check_primary(elements, add, mul, zero, I):
    if not check_ideal(elements, add, mul, zero, I): return False
    # must be proper
    if len(unique_elements(I)) == len(unique_elements(elements)): return False 
    
    for a in elements:
        for b in elements:
            if apply_op(mul, a, b) in I:
                if a in I: continue
                # check if b^n in I
                curr = b
                in_rad = False
                for _ in range(len(elements)):
                    if curr in I:
                        in_rad = True
                        break
                    curr = apply_op(mul, curr, b)
                if not in_rad:
                    return False
    return True

def get_radical(elements, mul, I):
    rad = []
    for x in elements:
        curr = x
        in_rad = False
        for _ in range(len(elements)):
            if curr in I:
                in_rad = True
                break
            curr = apply_op(mul, curr, x)
        if in_rad:
            rad.append(x)
    return unique_elements(rad)

def conditions(witness):
    try:
        R = get_attr(witness, 'R')
        S = get_attr(witness, 'S')
        add_R = get_attr(witness, 'add_R')
        mul_R = get_attr(witness, 'mul_R')
        add_S = get_attr(witness, 'add_S')
        mul_S = get_attr(witness, 'mul_S')
        f = get_attr(witness, 'f')
        Q = get_attr(witness, 'Q')
        P = get_attr(witness, 'P')
    except Exception:
        return [False, False, False]
        
    # H1: f is a ring homomorphism
    try:
        is_R, zero_R = check_ring(R, add_R, mul_R)
        is_S, zero_S = check_ring(S, add_S, mul_S)
        if not (is_R and is_S):
            h1 = False
        else:
            h1 = True
            for a in R:
                fa = apply_op(f, a)
                if fa not in S:
                    h1 = False
                    break
                for b in R:
                    fb = apply_op(f, b)
                    if apply_op(f, apply_op(add_R, a, b)) != apply_op(add_S, fa, fb):
                        h1 = False
                        break
                    if apply_op(f, apply_op(mul_R, a, b)) != apply_op(mul_S, fa, fb):
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: Q is a P-primary ideal of S
    try:
        if not h1:
            h2 = False
        else:
            is_prim = check_primary(S, add_S, mul_S, zero_S, Q)
            rad_Q = get_radical(S, mul_S, Q)
            
            same_elements = True
            for x in rad_Q:
                if x not in P:
                    same_elements = False
                    break
            for x in P:
                if x not in rad_Q:
                    same_elements = False
                    break
                    
            h2 = is_prim and same_elements
    except Exception:
        h2 = False

    # Neg_Q: f^{-1}(Q) is NOT an f^{-1}(P)-primary ideal in R
    try:
        if not h1:
            neg_q = False
        else:
            f_inv_Q = [x for x in R if apply_op(f, x) in Q]
            f_inv_P = [x for x in R if apply_op(f, x) in P]
            
            is_prim_inv = check_primary(R, add_R, mul_R, zero_R, f_inv_Q)
            rad_inv = get_radical(R, mul_R, f_inv_Q)
            
            same_elements_inv = True
            for x in rad_inv:
                if x not in f_inv_P:
                    same_elements_inv = False
                    break
            for x in f_inv_P:
                if x not in rad_inv:
                    same_elements_inv = False
                    break
            
            conclusion_holds = is_prim_inv and same_elements_inv
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
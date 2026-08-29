import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def apply_op(op, a, b):
    if callable(op):
        return op(a, b)
    return op[(a, b)]

def apply_f(f, x):
    if callable(f):
        return f(x)
    return f[x]

def is_ring_with_identity(elements, add, mult):
    try:
        elements = list(elements)
        for a in elements:
            for b in elements:
                if apply_op(add, a, b) not in elements: return False
                if apply_op(mult, a, b) not in elements: return False
        for a in elements:
            for b in elements:
                if apply_op(add, a, b) != apply_op(add, b, a): return False
                for c in elements:
                    if apply_op(add, apply_op(add, a, b), c) != apply_op(add, a, apply_op(add, b, c)): return False
                    if apply_op(mult, apply_op(mult, a, b), c) != apply_op(mult, a, apply_op(mult, b, c)): return False
                    if apply_op(mult, a, apply_op(add, b, c)) != apply_op(add, apply_op(mult, a, b), apply_op(mult, a, c)): return False
                    if apply_op(mult, apply_op(add, a, b), c) != apply_op(add, apply_op(mult, a, c), apply_op(mult, b, c)): return False
        zeros_list = [z for z in elements if all(apply_op(add, z, a) == a for a in elements)]
        if len(zeros_list) != 1: return False
        zero = zeros_list[0]
        for a in elements:
            if not any(apply_op(add, a, b) == zero for b in elements): return False
        ones_list = [u for u in elements if all(apply_op(mult, u, a) == a and apply_op(mult, a, u) == a for a in elements)]
        if len(ones_list) != 1: return False
        return True
    except Exception:
        return False

def get_zero_one(elements, add, mult):
    elements = list(elements)
    zeros_list = [z for z in elements if all(apply_op(add, z, a) == a for a in elements)]
    ones_list = [u for u in elements if all(apply_op(mult, u, a) == a and apply_op(mult, a, u) == a for a in elements)]
    return (zeros_list[0] if zeros_list else None, ones_list[0] if ones_list else None)

def get_units(elements, mult, one):
    elements = list(elements)
    units = []
    for a in elements:
        for b in elements:
            if apply_op(mult, a, b) == one and apply_op(mult, b, a) == one:
                units.append(a)
                break
    return units

def get_neg(elements, add, zero, a):
    elements = list(elements)
    for b in elements:
        if apply_op(add, a, b) == zero and apply_op(add, b, a) == zero:
            return b
    return None

def conditions(witness) -> list[bool]:
    try:
        R = witness['R']
        S = witness['S']
        R_add = witness['R_add']
        R_mult = witness['R_mult']
        S_add = witness['S_add']
        S_mult = witness['S_mult']
        f = witness['f']
    except Exception:
        return [False, False, False]

    try:
        h1_ok = is_ring_with_identity(R, R_add, R_mult) and is_ring_with_identity(S, S_add, S_mult)
    except Exception:
        h1_ok = False

    try:
        R_zero, R_one = get_zero_one(R, R_add, R_mult)
        S_zero, S_one = get_zero_one(S, S_add, S_mult)
        
        if R_one is None or S_one is None:
            h2_ok = False
        else:
            R_units = get_units(R, R_mult, R_one)
            S_units = get_units(S, S_mult, S_one)
            
            h2_ok = True
            for u in R_units:
                if apply_f(f, u) not in S_units:
                    h2_ok = False
                    break
            
            if h2_ok:
                for u in R_units:
                    for v in R_units:
                        if apply_f(f, apply_op(R_mult, u, v)) != apply_op(S_mult, apply_f(f, u), apply_f(f, v)):
                            h2_ok = False
                            break
                    if not h2_ok:
                        break
    except Exception:
        h2_ok = False

    try:
        R_zero, R_one = get_zero_one(R, R_add, R_mult)
        S_zero, S_one = get_zero_one(S, S_add, S_mult)
        if R_zero is None or R_one is None or S_zero is None or S_one is None:
            neg_q_ok = False
        else:
            R_units = get_units(R, R_mult, R_one)
            minus_one = get_neg(R, R_add, R_zero, R_one)
            
            ker_f_times = []
            for u in R_units:
                if apply_f(f, u) == S_one:
                    ker_f_times.append(u)
                    
            u_minus_1_in_ker_f = []
            for u in R_units:
                u_minus_1 = apply_op(R_add, u, minus_one)
                if apply_f(f, u_minus_1) == S_zero:
                    u_minus_1_in_ker_f.append(u)
                    
            def is_in(x, lst):
                return any(x == y for y in lst)
                
            same_sets = True
            for x in ker_f_times:
                if not is_in(x, u_minus_1_in_ker_f):
                    same_sets = False
                    break
            if same_sets:
                for x in u_minus_1_in_ker_f:
                    if not is_in(x, ker_f_times):
                        same_sets = False
                        break
                        
            neg_q_ok = not same_sets
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f^x: R^x -> S^x is the induced group homomorphism on the groups of units",
    "¬Q: The kernel of f^x is NOT the subgroup of R^x consisting of all units u in R^x such that u - 1 in ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2
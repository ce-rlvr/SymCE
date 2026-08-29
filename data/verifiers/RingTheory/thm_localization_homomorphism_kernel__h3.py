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

def _make_callable_2(op):
    if isinstance(op, dict):
        return lambda a, b: op[(a, b)]
    return op

def _make_callable_1(op):
    if isinstance(op, dict):
        return lambda a: op[a]
    return op

def is_commutative_ring(R_list, add, mul, zero, one=None):
    # check closure
    for a in R_list:
        for b in R_list:
            if add(a, b) not in R_list: return False
            if mul(a, b) not in R_list: return False
    
    # check add commutative
    for a in R_list:
        for b in R_list:
            if add(a, b) != add(b, a): return False
            
    # check add associative
    for a in R_list:
        for b in R_list:
            for c in R_list:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                
    # check zero
    for a in R_list:
        if add(a, zero) != a: return False
        
    # check add inverse
    for a in R_list:
        has_inv = False
        for b in R_list:
            if add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    # check mul commutative
    for a in R_list:
        for b in R_list:
            if mul(a, b) != mul(b, a): return False
            
    # check mul associative
    for a in R_list:
        for b in R_list:
            for c in R_list:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                
    # check distributivity
    for a in R_list:
        for b in R_list:
            for c in R_list:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                
    if one is not None:
        if one not in R_list: return False
        for a in R_list:
            if mul(a, one) != a: return False
            if mul(one, a) != a: return False
            
    return True

def is_mult_closed(R_list, mul, S):
    for s in S:
        if s not in R_list: return False
    for s1 in S:
        for s2 in S:
            if mul(s1, s2) not in S: return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            add = _make_callable_2(witness['add'])
            mul = _make_callable_2(witness['mul'])
            zero = witness['zero']
            one = witness.get('one', None)
        else:
            R = witness.R
            add = _make_callable_2(witness.add)
            mul = _make_callable_2(witness.mul)
            zero = witness.zero
            one = getattr(witness, 'one', None)
            
        R_list = list(R)
        if len(R_list) > 1000:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = is_commutative_ring(R_list, add, mul, zero, one)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            S = witness['S']
        else:
            S = witness.S
        h2 = is_mult_closed(R_list, mul, S)
    except Exception:
        h2 = False

    try:
        target_set = []
        for r in R_list:
            condition = False
            for s in S:
                if mul(s, r) == zero:
                    condition = True
                    break
            if condition:
                target_set.append(r)
                
        if isinstance(witness, dict) and 'f' in witness:
            f = _make_callable_1(witness['f'])
            f_zero = witness.get('f_zero', f(zero))
        elif hasattr(witness, 'f'):
            f = _make_callable_1(witness.f)
            f_zero = getattr(witness, 'f_zero', f(zero))
        else:
            f = None
            
        if f is not None:
            ker_f = []
            for r in R_list:
                if f(r) == f_zero:
                    ker_f.append(r)
            
            is_equal = True
            for r in R_list:
                if (r in ker_f) != (r in target_set):
                    is_equal = False
                    break
            neg_q = not is_equal
        else:
            # If f is not provided, the conclusion is false if the target set cannot be a valid kernel (e.g. doesn't contain zero)
            if zero not in target_set:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The kernel of f is not {r \in R | sr = 0 for some s \in S}"
]

N_HYP = 2
NEG_Q_INDEX = 2
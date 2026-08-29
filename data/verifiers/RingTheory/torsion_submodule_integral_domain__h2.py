import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import itertools
import functools
import math

# Top-level setup for standard algebra objects
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

def get_zero(elements, add_func):
    for z in elements:
        try:
            if all(add_func(a, z) == a and add_func(z, a) == a for a in elements):
                return z
        except Exception:
            continue
    return None

def get_one(elements, mult_func):
    for o in elements:
        try:
            if all(mult_func(a, o) == a and mult_func(o, a) == a for a in elements):
                return o
        except Exception:
            continue
    return None

def conditions(witness):
    def get_attr_or_key(obj, name, default=None):
        if isinstance(obj, dict):
            return obj.get(name, default)
        return getattr(obj, name, default)

    def safe_list(iterable, max_len=100):
        res = []
        for i, x in enumerate(iterable):
            if i >= max_len:
                raise ValueError("Iterable too long")
            res.append(x)
        return res

    try:
        if isinstance(witness, tuple):
            R_iter, R_add, R_mult, M_iter, M_add, smult, T_iter = witness[:7]
        else:
            R_iter = get_attr_or_key(witness, 'R')
            R_add = get_attr_or_key(witness, 'R_add')
            R_mult = get_attr_or_key(witness, 'R_mult')
            M_iter = get_attr_or_key(witness, 'M')
            M_add = get_attr_or_key(witness, 'M_add')
            smult = get_attr_or_key(witness, 'scalar_mult')
            T_iter = get_attr_or_key(witness, 'T')
            
        R = safe_list(R_iter)
        M = safe_list(M_iter)
        T = safe_list(T_iter)
    except Exception:
        return [False, False, False]
        
    R_zero = get_attr_or_key(witness, 'R_zero')
    if R_zero is None:
        R_zero = get_zero(R, R_add)
        
    R_one = get_attr_or_key(witness, 'R_one')
    if R_one is None:
        R_one = get_one(R, R_mult)
        
    M_zero = get_attr_or_key(witness, 'M_zero')
    if M_zero is None:
        M_zero = get_zero(M, M_add)

    def check_H1():
        if R_zero is None or R_one is None: return False
        if R_one == R_zero: return False
        if R_zero not in R or R_one not in R: return False
        
        for a in R:
            has_inv = False
            for b in R:
                if R_add(a, b) == R_zero and R_add(b, a) == R_zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in R:
                if R_add(a, b) not in R: return False
                if R_mult(a, b) not in R: return False
                if R_add(a, b) != R_add(b, a): return False
                if R_mult(a, b) != R_mult(b, a): return False
                if R_mult(a, b) == R_zero and a != R_zero and b != R_zero: return False
                
                for c in R:
                    if R_add(R_add(a, b), c) != R_add(a, R_add(b, c)): return False
                    if R_mult(R_mult(a, b), c) != R_mult(a, R_mult(b, c)): return False
                    if R_mult(a, R_add(b, c)) != R_add(R_mult(a, b), R_mult(a, c)): return False
        return True

    def check_H2():
        if M_zero is None: return False
        expected_T = []
        for m in M:
            is_torsion = False
            for r in R:
                if r != R_zero and smult(r, m) == M_zero:
                    is_torsion = True
                    break
            if is_torsion:
                expected_T.append(m)
                
        def unique(lst):
            res = []
            for x in lst:
                if x not in res:
                    res.append(x)
            return res
            
        T_u = unique(T)
        expected_T_u = unique(expected_T)
        
        if len(T_u) != len(expected_T_u): return False
        for t in expected_T_u:
            if t not in T_u: return False
        for t in T_u:
            if t not in expected_T_u: return False
        return True

    def check_neg_Q():
        if M_zero is None: return True
        if M_zero not in T: return True
        
        for t in T:
            if t not in M: return True
            
            has_inv = False
            for inv in T:
                if M_add(t, inv) == M_zero and M_add(inv, t) == M_zero:
                    has_inv = True
                    break
            if not has_inv: return True
            
            for r in R:
                if smult(r, t) not in T: return True
                
            for t2 in T:
                if M_add(t, t2) not in T: return True
                
        for t in T:
            if smult(R_one, t) != t: return True
            for t2 in T:
                if M_add(t, t2) != M_add(t2, t): return True
                for t3 in T:
                    if M_add(M_add(t, t2), t3) != M_add(t, M_add(t2, t3)): return True
                    
            for r in R:
                for t2 in T:
                    if smult(r, M_add(t, t2)) != M_add(smult(r, t), smult(r, t2)): return True
                for r2 in R:
                    if smult(R_add(r, r2), t) != M_add(smult(r, t), smult(r2, t)): return True
                    if smult(R_mult(r, r2), t) != smult(r, smult(r2, t)): return True
                    
        return False

    try:
        h1 = check_H1()
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2()
    except Exception:
        h2 = False
        
    try:
        neg_q = check_neg_Q()
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: T is the set of all m in M such that there exists a non-zero r in R with rm = 0",
    "¬Q: T is not a submodule of M"
]

N_HYP = 2
NEG_Q_INDEX = 2
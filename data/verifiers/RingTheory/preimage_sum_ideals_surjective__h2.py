import itertools
import math
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
from sympy.matrices import eye, zeros, Matrix

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def find_zero(R_set, R_add):
    for e in R_set:
        if all(R_add(e, a) == a and R_add(a, e) == a for a in R_set):
            return e
    return None

def find_one(R_set, R_mul):
    for e in R_set:
        if all(R_mul(e, a) == a and R_mul(a, e) == a for a in R_set):
            return e
    return None

def is_ring(R_set, R_add, R_mul):
    if not R_set: return False
    
    # closure
    for a in R_set:
        for b in R_set:
            try:
                if R_add(a, b) not in R_set: return False
                if R_mul(a, b) not in R_set: return False
            except Exception:
                return False
            
    # commutativity of addition
    for a in R_set:
        for b in R_set:
            if R_add(a, b) != R_add(b, a): return False
            
    # associativity and distributivity
    for a in R_set:
        for b in R_set:
            ab_add = R_add(a, b)
            ab_mul = R_mul(a, b)
            for c in R_set:
                if R_add(ab_add, c) != R_add(a, R_add(b, c)): return False
                if R_mul(ab_mul, c) != R_mul(a, R_mul(b, c)): return False
                if R_mul(a, R_add(b, c)) != R_add(ab_mul, R_mul(a, c)): return False
                if R_mul(ab_add, c) != R_add(R_mul(a, c), R_mul(b, c)): return False
                
    zero = find_zero(R_set, R_add)
    if zero is None: return False
    
    # inverses
    for a in R_set:
        if not any(R_add(a, b) == zero for b in R_set): return False
        
    one = find_one(R_set, R_mul)
    if one is None: return False
    
    return True

def is_homomorphism(R_set, S_set, R_add, R_mul, S_add, S_mul, f):
    one_R = find_one(R_set, R_mul)
    one_S = find_one(S_set, S_mul)
    if one_R is None or one_S is None: return False
    try:
        if f(one_R) != one_S: return False
    except Exception:
        return False
    
    for a in R_set:
        try:
            fa = f(a)
        except Exception:
            return False
        if fa not in S_set: return False
        for b in R_set:
            if f(R_add(a, b)) != S_add(fa, f(b)): return False
            if f(R_mul(a, b)) != S_mul(fa, f(b)): return False
    return True

def is_ideal(I, S_set, S_add, S_mul):
    if not I: return False
    if any(a not in S_set for a in I): return False
    
    zero = find_zero(S_set, S_add)
    if zero not in I: return False
    
    # closed under addition
    for a in I:
        for b in I:
            if S_add(a, b) not in I: return False
            
    # closed under inverses
    for a in I:
        has_inv = False
        for b in I:
            if S_add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    # closed under multiplication by S
    for i in I:
        for s in S_set:
            if S_mul(i, s) not in I: return False
            if S_mul(s, i) not in I: return False
            
    return True

def sum_ideals(I, J, S_add):
    res = []
    for i in I:
        for j in J:
            s = S_add(i, j)
            if s not in res:
                res.append(s)
    return res

def preimage(A, R_set, f):
    return [x for x in R_set if f(x) in A]

def sum_sets(A, B, R_add):
    res = []
    for a in A:
        for b in B:
            s = R_add(a, b)
            if s not in res:
                res.append(s)
    return res

def conditions(witness) -> list[bool]:
    try:
        R_set = witness['R_set']
        S_set = witness['S_set']
        
        raw_R_add = witness['R_add']
        R_add = (lambda a, b: raw_R_add[(a, b)]) if isinstance(raw_R_add, dict) else raw_R_add
        
        raw_R_mul = witness['R_mul']
        R_mul = (lambda a, b: raw_R_mul[(a, b)]) if isinstance(raw_R_mul, dict) else raw_R_mul
        
        raw_S_add = witness['S_add']
        S_add = (lambda a, b: raw_S_add[(a, b)]) if isinstance(raw_S_add, dict) else raw_S_add
        
        raw_S_mul = witness['S_mul']
        S_mul = (lambda a, b: raw_S_mul[(a, b)]) if isinstance(raw_S_mul, dict) else raw_S_mul
        
        raw_f = witness['f']
        f = (lambda a: raw_f[a]) if isinstance(raw_f, dict) else raw_f
        
        I = witness['I']
        J = witness['J']
    except (TypeError, KeyError, Exception):
        return [False, False, False]
        
    try:
        h1 = is_ring(R_set, R_add, R_mul) and is_ring(S_set, S_add, S_mul) and is_homomorphism(R_set, S_set, R_add, R_mul, S_add, S_mul, f)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ideal(I, S_set, S_add, S_mul) and is_ideal(J, S_set, S_add, S_mul)
    except Exception:
        h2 = False
        
    try:
        I_plus_J = sum_ideals(I, J, S_add)
        pre_I_plus_J = preimage(I_plus_J, R_set, f)
        
        pre_I = preimage(I, R_set, f)
        pre_J = preimage(J, R_set, f)
        sum_pre = sum_sets(pre_I, pre_J, R_add)
        
        def subset(A, B):
            return all(a in B for a in A)
            
        neg_q = not (subset(pre_I_plus_J, sum_pre) and subset(sum_pre, pre_I_plus_J))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings, and f is a ring homomorphism from R to S",
    "H_2: I and J are ideals of S",
    "¬Q: The preimage f^{-1}(I + J) is not equal to f^{-1}(I) + f^{-1}(J)"
]

N_HYP = 2
NEG_Q_INDEX = 2
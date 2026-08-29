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

def get_attr(w, name):
    if isinstance(w, dict):
        return w[name]
    return getattr(w, name)

def contains(lst, item):
    for x in lst:
        if x == item: 
            return True
    return False

def check_h1(witness):
    R = get_attr(witness, 'R')
    add_R = get_attr(witness, 'add_R')
    mul_R = get_attr(witness, 'mul_R')
    M = get_attr(witness, 'M')
    add_M = get_attr(witness, 'add_M')
    action = get_attr(witness, 'action')
    
    if not R or not M: 
        return False
    
    for a in R:
        for b in R:
            if not contains(R, add_R(a, b)): return False
            if not contains(R, mul_R(a, b)): return False
            
    for a in R:
        for b in R:
            if add_R(a, b) != add_R(b, a): return False
            for c in R:
                if add_R(add_R(a, b), c) != add_R(a, add_R(b, c)): return False
                if mul_R(mul_R(a, b), c) != mul_R(a, mul_R(b, c)): return False
                
    zeros_R = [z for z in R if all(add_R(a, z) == a for a in R)]
    if not zeros_R: return False
    zero_R = zeros_R[0]
    
    for a in R:
        has_inv = False
        for b in R:
            if add_R(a, b) == zero_R:
                has_inv = True
                break
        if not has_inv: return False
        
    for a in R:
        for b in R:
            for c in R:
                if mul_R(a, add_R(b, c)) != add_R(mul_R(a, b), mul_R(a, c)): return False
                if mul_R(add_R(a, b), c) != add_R(mul_R(a, c), mul_R(b, c)): return False
                
    for x in M:
        for y in M:
            if not contains(M, add_M(x, y)): return False
            if add_M(x, y) != add_M(y, x): return False
            for z in M:
                if add_M(add_M(x, y), z) != add_M(x, add_M(y, z)): return False
                
    zeros_M = [z for z in M if all(add_M(x, z) == x for x in M)]
    if not zeros_M: return False
    zero_M = zeros_M[0]
    
    for x in M:
        has_inv = False
        for y in M:
            if add_M(x, y) == zero_M:
                has_inv = True
                break
        if not has_inv: return False
        
    for r in R:
        for m in M:
            if not contains(M, action(r, m)): return False
            
    for r in R:
        for m1 in M:
            for m2 in M:
                if action(r, add_M(m1, m2)) != add_M(action(r, m1), action(r, m2)): return False
                
    for r1 in R:
        for r2 in R:
            for m in M:
                if action(add_R(r1, r2), m) != add_M(action(r1, m), action(r2, m)): return False
                if action(mul_R(r1, r2), m) != action(r1, action(r2, m)): return False
                
    return True

def check_h2(witness):
    R = get_attr(witness, 'R')
    add_R = get_attr(witness, 'add_R')
    mul_R = get_attr(witness, 'mul_R')
    I = get_attr(witness, 'I')
    J = get_attr(witness, 'J')
    
    if not I or not J: 
        return False
    
    for i in I:
        if not contains(R, i): return False
        for j in I:
            if not contains(I, add_R(i, j)): return False
            
    zeros_R = [z for z in R if all(add_R(a, z) == a for a in R)]
    if not zeros_R: return False
    zero_R = zeros_R[0]
    
    for i in I:
        has_inv = False
        for j in I:
            if add_R(i, j) == zero_R:
                has_inv = True
                break
        if not has_inv: return False
        
    for i in I:
        for r in R:
            if not contains(I, mul_R(r, i)): return False
            if not contains(I, mul_R(i, r)): return False
            
    for j in J:
        if not contains(R, j): return False
        for k in J:
            if not contains(J, add_R(j, k)): return False
            
    for j in J:
        has_inv = False
        for k in J:
            if add_R(j, k) == zero_R:
                has_inv = True
                break
        if not has_inv: return False
        
    for j in J:
        for r in R:
            if not contains(J, mul_R(r, j)): return False
            if not contains(J, mul_R(j, r)): return False
            
    for r in R:
        found = False
        for i in I:
            for j in J:
                if add_R(i, j) == r:
                    found = True
                    break
            if found: break
        if not found: return False
        
    return True

def check_neg_q(witness):
    R = get_attr(witness, 'R')
    M = get_attr(witness, 'M')
    add_M = get_attr(witness, 'add_M')
    action = get_attr(witness, 'action')
    I = get_attr(witness, 'I')
    J = get_attr(witness, 'J')
    
    I_cap_J = [x for x in I if contains(J, x)]
    
    zeros_M = [z for z in M if all(add_M(x, z) == x for x in M)]
    if not zeros_M: return False
    zero_M = zeros_M[0]
    
    def ann(ideal):
        res = []
        for m in M:
            is_ann = True
            for i in ideal:
                if action(i, m) != zero_M:
                    is_ann = False
                    break
            if is_ann:
                res.append(m)
        return res

    ann_I_cap_J = ann(I_cap_J)
    ann_I = ann(I)
    ann_J = ann(J)
    
    for x in ann_I_cap_J:
        found = False
        for a in ann_I:
            for b in ann_J:
                if add_M(a, b) == x:
                    found = True
                    break
            if found: break
        if not found: return True
        
    for a in ann_I:
        for b in ann_J:
            s = add_M(a, b)
            found = False
            for x in ann_I_cap_J:
                if x == s:
                    found = True
                    break
            if not found: return True
            
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = check_h1(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = check_h2(witness)
    except Exception:
        h2 = False
        
    try:
        neg_q = check_neg_q(witness)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "H_2: I and J are comaximal ideals of R",
    "¬Q: Ann_M(I \\cap J) != Ann_M(I) + Ann_M(J)"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import itertools
import math
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def unique(A):
    res = []
    for a in A:
        if a not in res:
            res.append(a)
    return res

def is_subset(A, B):
    for a in A:
        if a not in B: return False
    return True

def subset_add(A, B, add):
    res = []
    for a in A:
        for b in B:
            val = add(a, b)
            if val not in res:
                res.append(val)
    return unique(res)

def subset_mul(A, B, add, mul, zero):
    prods = []
    for a in A:
        for b in B:
            val = mul(a, b)
            if val not in prods:
                prods.append(val)
    
    closed = list(prods)
    if zero not in closed:
        closed.append(zero)
    changed = True
    while changed:
        changed = False
        n = len(closed)
        for i in range(n):
            for j in range(i, n):
                val = add(closed[i], closed[j])
                if val not in closed:
                    closed.append(val)
                    changed = True
    return closed

def subset_eq(A, B):
    A_u = unique(A)
    B_u = unique(B)
    if len(A_u) != len(B_u): return False
    for a in A_u:
        if a not in B_u: return False
    return True

def is_ring(R, add, mul, zero):
    if not isinstance(R, (list, tuple, set)): return False
    if not R: return False
    if zero is None: return False
    if len(R) > 200: return False
        
    for a in R:
        if add(a, zero) != a or add(zero, a) != a: return False
        has_inv = False
        for b in R:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False

    for a in R:
        for b in R:
            if add(a, b) not in R: return False
            if mul(a, b) not in R: return False
            if add(a, b) != add(b, a): return False

    sample = R[:20] if len(R) > 20 else R
    for a in sample:
        for b in sample:
            for c in sample:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
    return True

def is_ideal(R, J, add, mul, zero):
    if not isinstance(J, (list, tuple, set)): return False
    if not J: return False
    if zero not in J: return False
    
    for a in J:
        for b in J:
            if add(a, b) not in J: return False
        has_inv = False
        for b in J:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for r in R:
        for j in J:
            if mul(r, j) not in J: return False
            if mul(j, r) not in J: return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R', [])
            I = witness.get('I', [])
            J = witness.get('J', [])
            K = witness.get('K', [])
            add = witness.get('add', lambda a, b: a + b)
            mul = witness.get('mul', lambda a, b: a * b)
            zero = witness.get('zero', None)
        elif isinstance(witness, tuple) and len(witness) == 4:
            R, I, J, K = witness
            add = lambda a, b: a + b
            mul = lambda a, b: a * b
            zero = None
        else:
            return [False, False, False, False]
            
        R_u = unique(list(R))
        I_u = unique(list(I))
        J_u = unique(list(J))
        K_u = unique(list(K))
        
        if zero is None:
            for z in R_u:
                try:
                    if all(add(z, a) == a for a in R_u) and all(add(a, z) == a for a in R_u):
                        zero = z
                        break
                except Exception:
                    pass
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_ring(R_u, add, mul, zero)
    except Exception:
        h1 = False

    try:
        h2 = is_subset(J_u, R_u) and is_ideal(R_u, J_u, add, mul, zero)
    except Exception:
        h2 = False

    try:
        h3 = is_subset(K_u, R_u) and is_ideal(R_u, K_u, add, mul, zero)
    except Exception:
        h3 = False

    try:
        if not is_subset(I_u, R_u):
            neg_q = False
        else:
            J_plus_K = subset_add(J_u, K_u, add)
            I_J_plus_K = subset_mul(I_u, J_plus_K, add, mul, zero)
            
            IJ = subset_mul(I_u, J_u, add, mul, zero)
            IK = subset_mul(I_u, K_u, add, mul, zero)
            IJ_plus_IK = subset_add(IJ, IK, add)
            
            I_plus_J = subset_add(I_u, J_u, add)
            I_plus_J_K = subset_mul(I_plus_J, K_u, add, mul, zero)
            
            JK = subset_mul(J_u, K_u, add, mul, zero)
            IK_plus_JK = subset_add(IK, JK, add)
            
            eq1 = subset_eq(I_J_plus_K, IJ_plus_IK)
            eq2 = subset_eq(I_plus_J_K, IK_plus_JK)
            
            neg_q = not (eq1 and eq2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: J is an ideal of R",
    "H_3: K is an ideal of R",
    "¬Q: I(J + K) != IJ + IK or (I + J)K != IK + JK"
]

N_HYP = 3
NEG_Q_INDEX = 3
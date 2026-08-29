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

def check_abelian_group(elements, add, zero):
    # closure
    for a in elements:
        for b in elements:
            try:
                if add(a, b) not in elements: return False
            except Exception:
                return False
    # identity
    for a in elements:
        if add(a, zero) != a: return False
        if add(zero, a) != a: return False
    # inverses
    for a in elements:
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
    # associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
    # commutativity
    for a in elements:
        for b in elements:
            if add(a, b) != add(b, a): return False
    return True

def check_H1(w):
    R = get_attr(w, 'R')
    R_add = get_attr(w, 'R_add')
    R_mul = get_attr(w, 'R_mul')
    R_zero = get_attr(w, 'R_zero')
    R_one = get_attr(w, 'R_one')
    
    if not check_abelian_group(R, R_add, R_zero): return False
    
    # mul closure
    for a in R:
        for b in R:
            if R_mul(a, b) not in R: return False
            
    # mul associativity
    for a in R:
        for b in R:
            for c in R:
                if R_mul(R_mul(a, b), c) != R_mul(a, R_mul(b, c)): return False
                
    # mul identity
    for a in R:
        if R_mul(a, R_one) != a: return False
        if R_mul(R_one, a) != a: return False
        
    # distributivity
    for a in R:
        for b in R:
            for c in R:
                if R_mul(a, R_add(b, c)) != R_add(R_mul(a, b), R_mul(a, c)): return False
                if R_mul(R_add(a, b), c) != R_add(R_mul(a, c), R_mul(b, c)): return False
                
    return True

def check_H2(w):
    R = get_attr(w, 'R')
    M = get_attr(w, 'M')
    R_add = get_attr(w, 'R_add')
    R_mul = get_attr(w, 'R_mul')
    M_add = get_attr(w, 'M_add')
    M_zero = get_attr(w, 'M_zero')
    left_mul = get_attr(w, 'left_mul')
    right_mul = get_attr(w, 'right_mul')
    
    if not check_abelian_group(M, M_add, M_zero): return False
    
    # scalar mul closure
    for a in R:
        for x in M:
            if left_mul(a, x) not in M: return False
            if right_mul(x, a) not in M: return False

    # left_mul over M_add
    for a in R:
        for x in M:
            for y in M:
                if left_mul(a, M_add(x, y)) != M_add(left_mul(a, x), left_mul(a, y)): return False

    # left_mul over R_add
    for a in R:
        for b in R:
            for x in M:
                if left_mul(R_add(a, b), x) != M_add(left_mul(a, x), left_mul(b, x)): return False

    # left_mul over R_mul
    for a in R:
        for b in R:
            for x in M:
                if left_mul(R_mul(a, b), x) != left_mul(a, left_mul(b, x)): return False

    # right_mul over M_add
    for a in R:
        for x in M:
            for y in M:
                if right_mul(M_add(x, y), a) != M_add(right_mul(x, a), right_mul(y, a)): return False

    # right_mul over R_add
    for a in R:
        for b in R:
            for x in M:
                if right_mul(x, R_add(a, b)) != M_add(right_mul(x, a), right_mul(x, b)): return False

    # right_mul over R_mul
    for a in R:
        for b in R:
            for x in M:
                if right_mul(x, R_mul(a, b)) != right_mul(right_mul(x, a), b): return False

    # compatibility
    for a in R:
        for b in R:
            for x in M:
                if left_mul(a, right_mul(x, b)) != right_mul(left_mul(a, x), b): return False

    return True

def check_H3(w):
    R = get_attr(w, 'R')
    M = get_attr(w, 'M')
    r = get_attr(w, 'r')
    m = get_attr(w, 'm')
    return (r in R) and (m in M)

def check_neg_Q(w):
    R = get_attr(w, 'R')
    M = get_attr(w, 'M')
    r = get_attr(w, 'r')
    m = get_attr(w, 'm')
    R_add = get_attr(w, 'R_add')
    R_mul = get_attr(w, 'R_mul')
    R_one = get_attr(w, 'R_one')
    M_add = get_attr(w, 'M_add')
    left_mul = get_attr(w, 'left_mul')
    right_mul = get_attr(w, 'right_mul')
    
    # Check if r is a unit in R
    r_is_unit = False
    for s in R:
        if R_mul(r, s) == R_one and R_mul(s, r) == R_one:
            r_is_unit = True
            break
            
    # Find identity of R \ltimes M
    id_RM = None
    for e_r in R:
        for e_m in M:
            is_id = True
            for a in R:
                for x in M:
                    # (e_r, e_m) * (a, x)
                    p1_r = R_mul(e_r, a)
                    p1_m = M_add(left_mul(e_r, x), right_mul(e_m, a))
                    if p1_r != a or p1_m != x:
                        is_id = False
                        break
                    # (a, x) * (e_r, e_m)
                    p2_r = R_mul(a, e_r)
                    p2_m = M_add(left_mul(a, e_m), right_mul(x, e_r))
                    if p2_r != a or p2_m != x:
                        is_id = False
                        break
                if not is_id:
                    break
            if is_id:
                id_RM = (e_r, e_m)
                break
        if id_RM is not None:
            break
            
    # Check if (r, m) is a unit in R \ltimes M
    rm_is_unit = False
    if id_RM is not None:
        e_r, e_m = id_RM
        for s in R:
            for n in M:
                p1_r = R_mul(r, s)
                p1_m = M_add(left_mul(r, n), right_mul(m, s))
                if p1_r == e_r and p1_m == e_m:
                    p2_r = R_mul(s, r)
                    p2_m = M_add(left_mul(s, m), right_mul(n, r))
                    if p2_r == e_r and p2_m == e_m:
                        rm_is_unit = True
                        break
            if rm_is_unit:
                break
                
    # The conclusion is: rm_is_unit <==> r_is_unit
    # We want the conclusion to FAIL, so they must be different
    return rm_is_unit != r_is_unit

def conditions(witness):
    try:
        h1 = check_H1(witness)
    except Exception:
        h1 = False

    try:
        h2 = check_H2(witness)
    except Exception:
        h2 = False

    try:
        h3 = check_H3(witness)
    except Exception:
        h3 = False

    try:
        neg_q = check_neg_Q(witness)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unital ring",
    "H_2: M is an R-bimodule",
    "H_3: (r, m) is an element of R \\ltimes M",
    "¬Q: (r, m) is a unit in R \\ltimes M iff r is a unit in R is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3
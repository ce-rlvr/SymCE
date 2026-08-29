import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

def is_ring_with_identity(elements, add, mul, zero, one):
    try:
        elements = list(elements)
    except Exception:
        return False
    if zero not in elements or one not in elements: return False
    for a in elements:
        if add(a, zero) != a or add(zero, a) != a: return False
        if mul(a, one) != a or mul(one, a) != a: return False
        # check additive inverse
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
        for b in elements:
            ab_add = add(a, b)
            ab_mul = mul(a, b)
            if ab_add not in elements: return False
            if ab_mul not in elements: return False
            if ab_add != add(b, a): return False
            for c in elements:
                if add(ab_add, c) != add(a, add(b, c)): return False
                if mul(ab_mul, c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(ab_mul, mul(a, c)): return False
                if mul(ab_add, c) != add(mul(a, c), mul(b, c)): return False
    return True

def conditions(witness):
    try:
        R = list(witness['R'])
        S = list(witness['S'])
        add_R = witness['add_R']
        mul_R = witness['mul_R']
        zero_R = witness['zero_R']
        one_R = witness['one_R']
        add_S = witness['add_S']
        mul_S = witness['mul_S']
        zero_S = witness['zero_S']
        one_S = witness['one_S']
        f = witness['f']
        u = witness['u']
    except Exception:
        return [False, False, False, False]

    # H1: R and S are rings with identity
    try:
        h1 = is_ring_with_identity(R, add_R, mul_R, zero_R, one_R) and \
             is_ring_with_identity(S, add_S, mul_S, zero_S, one_S)
    except Exception:
        h1 = False

    # H2: f maps R to S and f(1_R) = 1_S
    try:
        if callable(f):
            maps_R_to_S = all(f(x) in S for x in R)
            f_one = f(one_R)
        elif isinstance(f, dict):
            maps_R_to_S = all(x in f and f[x] in S for x in R)
            f_one = f.get(one_R)
        elif isinstance(f, (list, tuple)):
            try:
                f_dict = dict(f)
                maps_R_to_S = all(x in f_dict and f_dict[x] in S for x in R)
                f_one = f_dict.get(one_R)
                f = f_dict
            except Exception:
                maps_R_to_S = False
                f_one = None
        else:
            maps_R_to_S = False
            f_one = None
            
        h2 = maps_R_to_S and (f_one == one_S)
    except Exception:
        h2 = False

    # H3: u is a unit in R
    try:
        h3 = False
        if u in R:
            for v in R:
                if mul_R(u, v) == one_R and mul_R(v, u) == one_R:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # neg_Q: f(u) is not a unit in S or f(u^{-1}) != f(u)^{-1}
    try:
        neg_q = False
        if u in R:
            u_inv = None
            for v in R:
                if mul_R(u, v) == one_R and mul_R(v, u) == one_R:
                    u_inv = v
                    break
            
            if u_inv is not None:
                if callable(f):
                    f_u = f(u)
                    f_u_inv = f(u_inv)
                elif isinstance(f, dict):
                    f_u = f.get(u)
                    f_u_inv = f.get(u_inv)
                else:
                    f_u = None
                    f_u_inv = None
                
                if f_u in S:
                    f_u_is_unit = False
                    f_u_inverse = None
                    for w in S:
                        if mul_S(f_u, w) == one_S and mul_S(w, f_u) == one_S:
                            f_u_is_unit = True
                            f_u_inverse = w
                            break
                    
                    if not f_u_is_unit:
                        neg_q = True
                    else:
                        if f_u_inv != f_u_inverse:
                            neg_q = True
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f maps R to S and f(1_R) = 1_S",
    "H_3: u is a unit in R",
    "¬Q: f(u) is not a unit in S or f(u^{-1}) != f(u)^{-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3
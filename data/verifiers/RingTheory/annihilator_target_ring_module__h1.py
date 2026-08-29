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

def get_attr(w, name):
    if isinstance(w, dict):
        return w[name]
    return getattr(w, name)

def get_attr_default(w, name, default):
    try:
        if isinstance(w, dict):
            return w.get(name, default)
        return getattr(w, name, default)
    except Exception:
        return default

def is_ring(elements, add, mul, zero, one, eq):
    if not any(eq(zero, x) for x in elements): return False
    if not any(eq(one, x) for x in elements): return False
    
    for a in elements:
        for b in elements:
            if not any(eq(add(a, b), x) for x in elements): return False
            if not any(eq(mul(a, b), x) for x in elements): return False
            
    for a in elements:
        if not eq(add(a, zero), a) or not eq(add(zero, a), a): return False
        has_inv = False
        for b in elements:
            if eq(add(a, b), zero) and eq(add(b, a), zero):
                has_inv = True
                break
        if not has_inv: return False
        
        for b in elements:
            if not eq(add(a, b), add(b, a)): return False
            for c in elements:
                if not eq(add(add(a, b), c), add(a, add(b, c))): return False
                
    for a in elements:
        if not eq(mul(a, one), a) or not eq(mul(one, a), a): return False
        for b in elements:
            for c in elements:
                if not eq(mul(mul(a, b), c), mul(a, mul(b, c))): return False
                if not eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))): return False
                if not eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))): return False
    return True

def conditions(witness) -> list[bool]:
    try:
        R = get_attr(witness, 'R')
        S = get_attr(witness, 'S')
        f = get_attr(witness, 'f')
        add_R = get_attr(witness, 'add_R')
        mul_R = get_attr(witness, 'mul_R')
        add_S = get_attr(witness, 'add_S')
        mul_S = get_attr(witness, 'mul_S')
        zero_R = get_attr(witness, 'zero_R')
        zero_S = get_attr(witness, 'zero_S')
        one_R = get_attr(witness, 'one_R')
        one_S = get_attr(witness, 'one_S')
    except Exception:
        return [False, False, False, False]

    eq_R = get_attr_default(witness, 'eq_R', lambda a, b: a == b)
    eq_S = get_attr_default(witness, 'eq_S', lambda a, b: a == b)

    # H_1: f is a ring homomorphism from R to S
    h1 = True
    try:
        if not is_ring(R, add_R, mul_R, zero_R, one_R, eq_R):
            h1 = False
        if not is_ring(S, add_S, mul_S, zero_S, one_S, eq_S):
            h1 = False
            
        if h1:
            if not eq_S(f(zero_R), zero_S):
                h1 = False
            for a in R:
                if not any(eq_S(f(a), x) for x in S):
                    h1 = False
                    break
                for b in R:
                    if not eq_S(f(add_R(a, b)), add_S(f(a), f(b))):
                        h1 = False
                        break
                    if not eq_S(f(mul_R(a, b)), mul_S(f(a), f(b))):
                        h1 = False
                        break
                if not h1: break
    except Exception:
        h1 = False

    # H_2: f maps the multiplicative identity of R to the multiplicative identity of S
    h2 = True
    try:
        if not eq_S(f(one_R), one_S):
            h2 = False
    except Exception:
        h2 = False

    # H_3: S is equipped with a left R-module structure defined by r * s = f(r)s
    h3 = True
    try:
        def action(r, s):
            try:
                return get_attr(witness, 'action')(r, s)
            except Exception:
                return mul_S(f(r), s)
                
        for r in R:
            for s in S:
                if not eq_S(action(r, s), mul_S(f(r), s)):
                    h3 = False
                    break
            if not h3: break
            
        if h3:
            for r1 in R:
                for r2 in R:
                    for s in S:
                        if not eq_S(action(add_R(r1, r2), s), add_S(action(r1, s), action(r2, s))):
                            h3 = False
                            break
                        if not eq_S(action(mul_R(r1, r2), s), action(r1, action(r2, s))):
                            h3 = False
                            break
                    if not h3: break
                if not h3: break
                
        if h3:
            for r in R:
                for s1 in S:
                    for s2 in S:
                        if not eq_S(action(r, add_S(s1, s2)), add_S(action(r, s1), action(r, s2))):
                            h3 = False
                            break
                    if not h3: break
                    
        if h3:
            for s in S:
                if not eq_S(action(one_R, s), s):
                    h3 = False
                    break
    except Exception:
        h3 = False

    # ¬Q: The annihilator of S as an R-module is not exactly the kernel of f
    neg_q = False
    try:
        def action(r, s):
            try:
                return get_attr(witness, 'action')(r, s)
            except Exception:
                return mul_S(f(r), s)
                
        ann_S = []
        for r in R:
            if all(eq_S(action(r, s), zero_S) for s in S):
                ann_S.append(r)
                
        ker_f = []
        for r in R:
            if eq_S(f(r), zero_S):
                ker_f.append(r)
                
        q = True
        for r in ann_S:
            if not any(eq_R(r, k) for k in ker_f):
                q = False
                break
        if q:
            for r in ker_f:
                if not any(eq_R(r, a) for a in ann_S):
                    q = False
                    break
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: f maps the multiplicative identity of R to the multiplicative identity of S",
    "H_3: S is equipped with a left R-module structure defined by r * s = f(r)s for all r in R and s in S",
    "¬Q: The annihilator of S as an R-module is not exactly the kernel of f"
]

N_HYP = 3
NEG_Q_INDEX = 3
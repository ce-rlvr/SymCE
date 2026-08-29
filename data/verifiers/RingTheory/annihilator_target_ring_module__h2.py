import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def call_f(f, x):
    return f[x] if isinstance(f, dict) else f(x)

def conditions(witness):
    try:
        R = witness.R
        S = witness.S
        add_R = witness.add_R
        mul_R = witness.mul_R
        zero_R = witness.zero_R
        one_R = witness.one_R
        add_S = witness.add_S
        mul_S = witness.mul_S
        zero_S = witness.zero_S
        one_S = witness.one_S
        f = witness.f
    except Exception:
        return [False, False, False, False]

    def check_ring(elements, add, mul, zero, one):
        try:
            if zero not in elements or one not in elements: return False
            for a in elements:
                if add(a, zero) != a or add(zero, a) != a: return False
                if mul(a, one) != a or mul(one, a) != a: return False
                for b in elements:
                    if add(a, b) != add(b, a): return False
                    if add(a, b) not in elements: return False
                    if mul(a, b) not in elements: return False
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): return False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
            for a in elements:
                has_inv = False
                for b in elements:
                    if add(a, b) == zero:
                        has_inv = True
                        break
                if not has_inv: return False
            return True
        except Exception:
            return False

    try:
        h1 = check_ring(R, add_R, mul_R, zero_R, one_R) and check_ring(S, add_S, mul_S, zero_S, one_S)
    except Exception:
        h1 = False

    try:
        h2 = (call_f(f, one_R) == one_S)
    except Exception:
        h2 = False

    try:
        h3 = True
        for r in R:
            fr = call_f(f, r)
            if fr not in S:
                h3 = False
                break
            for s1 in S:
                for s2 in S:
                    lhs = mul_S(fr, add_S(s1, s2))
                    rhs = add_S(mul_S(fr, s1), mul_S(fr, s2))
                    if lhs != rhs: h3 = False
            if not h3: break
            
        if h3:
            for r1 in R:
                for r2 in R:
                    fr1 = call_f(f, r1)
                    fr2 = call_f(f, r2)
                    f_add = call_f(f, add_R(r1, r2))
                    f_mul = call_f(f, mul_R(r1, r2))
                    for s in S:
                        lhs = mul_S(f_add, s)
                        rhs = add_S(mul_S(fr1, s), mul_S(fr2, s))
                        if lhs != rhs: h3 = False
                        
                        lhs = mul_S(f_mul, s)
                        rhs = mul_S(fr1, mul_S(fr2, s))
                        if lhs != rhs: h3 = False
                    if not h3: break
                if not h3: break
                
        if h3:
            f_one = call_f(f, one_R)
            for s in S:
                if mul_S(f_one, s) != s: h3 = False
    except Exception:
        h3 = False

    try:
        Ann_S = []
        for r in R:
            is_ann = True
            fr = call_f(f, r)
            for s in S:
                if mul_S(fr, s) != zero_S:
                    is_ann = False
                    break
            if is_ann:
                Ann_S.append(r)
                
        ker_f = [r for r in R if call_f(f, r) == zero_S]
        
        q = True
        for r in Ann_S:
            if r not in ker_f: q = False
        for r in ker_f:
            if r not in Ann_S: q = False
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f maps the multiplicative identity of R to the multiplicative identity of S",
    "H_3: S is equipped with a left R-module structure defined by r * s = f(r)s",
    "¬Q: The annihilator of S as an R-module is not exactly the kernel of f"
]

N_HYP = 3
NEG_Q_INDEX = 3
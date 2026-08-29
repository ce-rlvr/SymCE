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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    def get_attr(w, name):
        if isinstance(w, dict) and name in w:
            return w[name]
        return getattr(w, name)

    def eq(a, b):
        if a is b:
            return True
        if a == b:
            return True
        if hasattr(a, 'equals'):
            try:
                res = a.equals(b)
                if res is not None:
                    return res
            except Exception:
                pass
        return False

    def is_in(a, lst):
        return any(eq(a, x) for x in lst)

    def make_callable_2(op):
        if isinstance(op, dict):
            def op_callable(a, b):
                for (k1, k2), v in op.items():
                    if eq(k1, a) and eq(k2, b):
                        return v
                return op[(a, b)]
            return op_callable
        return op

    def is_ring(elements, add, mul, zero):
        try:
            if not elements: return False
            if not is_in(zero, elements): return False
            if not all(eq(add(a, zero), a) and eq(add(zero, a), a) for a in elements): return False
            if not all(is_in(add(a, b), elements) for a in elements for b in elements): return False
            if not all(is_in(mul(a, b), elements) for a in elements for b in elements): return False
            if not all(eq(add(a, b), add(b, a)) for a in elements for b in elements): return False
            if not all(eq(add(add(a, b), c), add(a, add(b, c))) for a in elements for b in elements for c in elements): return False
            if not all(eq(mul(mul(a, b), c), mul(a, mul(b, c))) for a in elements for b in elements for c in elements): return False
            if not all(eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))) for a in elements for b in elements for c in elements): return False
            if not all(eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))) for a in elements for b in elements for c in elements): return False
            for a in elements:
                if not any(eq(add(a, b), zero) for b in elements): return False
            return True
        except Exception:
            return False

    try:
        R = list(get_attr(witness, 'R'))
        S = list(get_attr(witness, 'S'))
        
        add_R = make_callable_2(get_attr(witness, 'add_R'))
        mul_R = make_callable_2(get_attr(witness, 'mul_R'))
        add_S = make_callable_2(get_attr(witness, 'add_S'))
        mul_S = make_callable_2(get_attr(witness, 'mul_S'))
        
        zero_R = get_attr(witness, 'zero_R')
        zero_S = get_attr(witness, 'zero_S')
        
        f_raw = get_attr(witness, 'f')
        if isinstance(f_raw, dict):
            def f(x):
                for k, v in f_raw.items():
                    if eq(k, x):
                        return v
                return f_raw[x]
        else:
            f = f_raw
            
        I = list(get_attr(witness, 'I'))
    except Exception:
        return [False, False, False]

    # H1: f: R -> S is a surjective ring homomorphism
    h1_ok = False
    try:
        if is_ring(R, add_R, mul_R, zero_R) and is_ring(S, add_S, mul_S, zero_S):
            maps_to_S = all(is_in(f(r), S) for r in R)
            hom_add = all(eq(f(add_R(a, b)), add_S(f(a), f(b))) for a in R for b in R)
            hom_mul = all(eq(f(mul_R(a, b)), mul_S(f(a), f(b))) for a in R for b in R)
            surjective = all(any(eq(f(r), s) for r in R) for s in S)
            h1_ok = bool(maps_to_S and hom_add and hom_mul and surjective)
    except Exception:
        h1_ok = False

    # H2: I is a nil ideal of R
    h2_ok = False
    try:
        subset = all(is_in(x, R) for x in I)
        contains_zero = is_in(zero_R, I)
        closed_add = all(is_in(add_R(a, b), I) for a in I for b in I)
        has_inv = all(any(eq(add_R(a, b), zero_R) for b in I) for a in I)
        absorbing = all(is_in(mul_R(x, r), I) and is_in(mul_R(r, x), I) for x in I for r in R)
        
        max_n = max(100, len(R))
        def is_nil_R(x):
            curr = x
            if eq(curr, zero_R): return True
            for _ in range(max_n):
                curr = mul_R(curr, x)
                if eq(curr, zero_R): return True
            return False
            
        is_nil = all(is_nil_R(x) for x in I)
        
        h2_ok = bool(subset and contains_zero and closed_add and has_inv and absorbing and is_nil)
    except Exception:
        h2_ok = False

    # neg_Q: f(I) is NOT a nil ideal of S
    neg_q_ok = False
    try:
        f_I = []
        for x in I:
            fx = f(x)
            if not is_in(fx, f_I):
                f_I.append(fx)
                
        contains_zero_S = is_in(zero_S, f_I)
        closed_add_S = all(is_in(add_S(a, b), f_I) for a in f_I for b in f_I)
        has_inv_S = all(any(eq(add_S(a, b), zero_S) for b in f_I) for a in f_I)
        absorbing_S = all(is_in(mul_S(y, s), f_I) and is_in(mul_S(s, y), f_I) for y in f_I for s in S)
        
        is_ideal_S = contains_zero_S and closed_add_S and has_inv_S and absorbing_S
        
        max_n_S = max(100, len(S))
        def is_nil_S(y):
            curr = y
            if eq(curr, zero_S): return True
            for _ in range(max_n_S):
                curr = mul_S(curr, y)
                if eq(curr, zero_S): return True
            return False
            
        is_nil_fI = all(is_nil_S(y) for y in f_I)
        
        neg_q_ok = not (is_ideal_S and is_nil_fI)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f: R -> S is a surjective ring homomorphism",
    "H_2: I is a nil ideal of R",
    "¬Q: The image f(I) is not a nil ideal of S"
]

N_HYP = 2
NEG_Q_INDEX = 2
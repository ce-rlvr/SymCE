import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math
import z3

# Standard algebra objects
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

def conditions(witness) -> list[bool]:
    """
    Expects a witness dictionary with:
    - 'R': list of elements in ring R
    - 'S': list of elements in ring S
    - 'add_R': callable(a, b)
    - 'mul_R': callable(a, b)
    - 'add_S': callable(a, b)
    - 'mul_S': callable(a, b)
    - 'zero_R': additive identity of R
    - 'zero_S': additive identity of S
    - 'f': callable(a) or dict mapping R to S
    - 'I': list of elements in ideal I of R
    """
    try:
        R = list(witness['R'])
        S = list(witness['S'])
        add_R = witness['add_R']
        mul_R = witness['mul_R']
        add_S = witness['add_S']
        mul_S = witness['mul_S']
        zero_R = witness['zero_R']
        zero_S = witness['zero_S']
        f_map = witness['f']
        I = list(witness['I'])
    except (KeyError, TypeError):
        return [False] * 4 + [False]

    def apply_f(x):
        if isinstance(f_map, dict):
            return f_map[x]
        return f_map(x)

    def is_ring(elements, add, mul, zero):
        if zero not in elements: return False
        # check closure
        for a in elements:
            for b in elements:
                try:
                    if add(a, b) not in elements: return False
                    if mul(a, b) not in elements: return False
                except Exception:
                    return False
        # check add axioms
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a: return False
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in elements:
                if add(a, b) != add(b, a): return False
        
        # check associativity and distributivity
        for a in elements:
            for b in elements:
                ab_add = add(a, b)
                ab_mul = mul(a, b)
                for c in elements:
                    if add(ab_add, c) != add(a, add(b, c)): return False
                    if mul(ab_mul, c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(ab_mul, mul(a, c)): return False
                    if mul(ab_add, c) != add(mul(a, c), mul(b, c)): return False
        return True

    # H1: R is a ring
    try:
        h1 = is_ring(R, add_R, mul_R, zero_R)
    except Exception:
        h1 = False

    # H2: S is a ring
    try:
        h2 = is_ring(S, add_S, mul_S, zero_S)
    except Exception:
        h2 = False

    # H3: f is a ring homomorphism from R to S
    try:
        h3 = True
        for a in R:
            if apply_f(a) not in S:
                h3 = False
                break
            for b in R:
                if apply_f(add_R(a, b)) != add_S(apply_f(a), apply_f(b)):
                    h3 = False
                    break
                if apply_f(mul_R(a, b)) != mul_S(apply_f(a), apply_f(b)):
                    h3 = False
                    break
            if not h3: break
        if apply_f(zero_R) != zero_S:
            h3 = False
        
        # If both rings are unital, f must preserve the identity
        if h3:
            one_R = None
            for e in R:
                if all(mul_R(e, a) == a and mul_R(a, e) == a for a in R):
                    one_R = e
                    break
            one_S = None
            for e in S:
                if all(mul_S(e, a) == a and mul_S(a, e) == a for a in S):
                    one_S = e
                    break
            if one_R is not None and one_S is not None:
                if apply_f(one_R) != one_S:
                    h3 = False
    except Exception:
        h3 = False

    # H4: I is an ideal of R
    try:
        h4 = True
        if zero_R not in I:
            h4 = False
        for i in I:
            if i not in R:
                h4 = False
                break
            inv_found = False
            for j in I:
                if add_R(i, j) == zero_R and add_R(j, i) == zero_R:
                    inv_found = True
                    break
            if not inv_found:
                h4 = False
                break
            for j in I:
                if add_R(i, j) not in I:
                    h4 = False
                    break
            for r in R:
                if mul_R(i, r) not in I:
                    h4 = False
                    break
                if mul_R(r, i) not in I:
                    h4 = False
                    break
            if not h4: break
    except Exception:
        h4 = False

    # neg_Q: f(I) is NOT an ideal of S
    try:
        f_I = []
        for i in I:
            fi = apply_f(i)
            if fi not in f_I:
                f_I.append(fi)
        
        is_ideal = True
        if zero_S not in f_I:
            is_ideal = False
        else:
            for x in f_I:
                inv_found = False
                for y in f_I:
                    if add_S(x, y) == zero_S and add_S(y, x) == zero_S:
                        inv_found = True
                        break
                if not inv_found:
                    is_ideal = False
                    break
                for y in f_I:
                    if add_S(x, y) not in f_I:
                        is_ideal = False
                        break
                for s in S:
                    if mul_S(x, s) not in f_I:
                        is_ideal = False
                        break
                    if mul_S(s, x) not in f_I:
                        is_ideal = False
                        break
                if not is_ideal:
                    break
        neg_q = not is_ideal
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: S is a ring",
    "H_3: f is a ring homomorphism from R to S",
    "H_4: I is an ideal of R",
    "¬Q: f(I) is not an ideal of S"
]

N_HYP = 4
NEG_Q_INDEX = 4
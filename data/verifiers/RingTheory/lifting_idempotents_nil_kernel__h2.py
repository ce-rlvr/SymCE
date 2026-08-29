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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = list(witness['R'])
            S = list(witness['S'])
            add_R = witness['add_R']
            mul_R = witness['mul_R']
            zero_R = witness['zero_R']
            add_S = witness['add_S']
            mul_S = witness['mul_S']
            zero_S = witness['zero_S']
            f = witness['f']
            e = witness['e']
        else:
            R = list(witness.R)
            S = list(witness.S)
            add_R = witness.add_R
            mul_R = witness.mul_R
            zero_R = witness.zero_R
            add_S = witness.add_S
            mul_S = witness.mul_S
            zero_S = witness.zero_S
            f = witness.f
            e = witness.e
    except Exception:
        return [False, False, False, False]

    # H1: R and S are rings
    def is_ring(elements, add, mul, zero):
        if zero not in elements: return False
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a: return False
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in elements:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
                if add(a, b) != add(b, a): return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        return True

    try:
        h1 = is_ring(R, add_R, mul_R, zero_R) and is_ring(S, add_S, mul_S, zero_S)
    except Exception:
        h1 = False

    # H2: f is a ring homomorphism and its kernel is a nil ideal
    try:
        is_hom = True
        for a in R:
            if f(a) not in S:
                is_hom = False
                break
            for b in R:
                if f(add_R(a, b)) != add_S(f(a), f(b)):
                    is_hom = False
                    break
                if f(mul_R(a, b)) != mul_S(f(a), f(b)):
                    is_hom = False
                    break

        ker = [x for x in R if f(x) == zero_S]
        is_nil = True
        for x in ker:
            is_nilpotent = False
            curr = x
            for _ in range(len(R) + 1):
                if curr == zero_R:
                    is_nilpotent = True
                    break
                curr = mul_R(curr, x)
            if not is_nilpotent:
                is_nil = False
                break
        
        is_ideal = True
        for x in ker:
            for r in R:
                if mul_R(r, x) not in ker: is_ideal = False
                if mul_R(x, r) not in ker: is_ideal = False

        h2 = is_hom and is_nil and is_ideal
    except Exception:
        h2 = False

    # H3: e is an idempotent element in S
    try:
        h3 = (e in S) and (mul_S(e, e) == e)
    except Exception:
        h3 = False

    # Negated Conclusion: There is NO idempotent element E in R such that f(E) = e
    try:
        neg_q = True
        for E in R:
            if mul_R(E, E) == E:
                if f(E) == e:
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a ring homomorphism and its kernel is a nil ideal",
    "H_3: e is an idempotent element in S",
    "¬Q: There is no idempotent element E in R such that f(E) = e"
]

N_HYP = 3
NEG_Q_INDEX = 3
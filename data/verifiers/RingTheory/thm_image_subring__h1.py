import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
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

def contains(lst, item):
    for x in lst:
        try:
            if bool(x == item):
                return True
        except Exception:
            pass
    return False

def get_zero(ring):
    for e in ring:
        is_zero = True
        for x in ring:
            try:
                if not (bool(e + x == x) and bool(x + e == x)):
                    is_zero = False
                    break
            except Exception:
                is_zero = False
                break
        if is_zero:
            return e
    return None

def get_one(ring):
    for e in ring:
        is_one = True
        for x in ring:
            try:
                if not (bool(e * x == x) and bool(x * e == x)):
                    is_one = False
                    break
            except Exception:
                is_one = False
                break
        if is_one:
            return e
    return None

def is_ring(ring):
    if not ring: return False
    # closure and commutativity of +
    for x in ring:
        for y in ring:
            try:
                if not contains(ring, x + y): return False
                if not contains(ring, x * y): return False
                if not bool(x + y == y + x): return False
            except Exception:
                return False
    # associativity and distributivity
    for x in ring:
        for y in ring:
            for z in ring:
                try:
                    if not bool((x + y) + z == x + (y + z)): return False
                    if not bool((x * y) * z == x * (y * z)): return False
                    if not bool(x * (y + z) == (x * y) + (x * z)): return False
                    if not bool((x + y) * z == (x * z) + (y * z)): return False
                except Exception:
                    return False
    zero = get_zero(ring)
    if zero is None: return False
    for x in ring:
        has_inv = False
        for y in ring:
            try:
                if bool(x + y == zero):
                    has_inv = True
                    break
            except Exception:
                pass
        if not has_inv: return False
    one = get_one(ring)
    if one is None: return False
    return True

def apply_f(f, x):
    if callable(f):
        return f(x)
    elif isinstance(f, dict):
        try:
            return f[x]
        except (TypeError, KeyError):
            for k, v in f.items():
                if bool(k == x):
                    return v
            raise ValueError("Mapping not found")
    else:
        for k, v in f:
            if bool(k == x):
                return v
        raise ValueError("Mapping not found")

def is_homomorphism(f, R, S):
    for x in R:
        for y in R:
            try:
                fx = apply_f(f, x)
                fy = apply_f(f, y)
                if not contains(S, fx): return False
                if not contains(S, fy): return False
                if not bool(apply_f(f, x + y) == fx + fy): return False
                if not bool(apply_f(f, x * y) == fx * fy): return False
            except Exception:
                return False
    return True

def is_subring(A, R):
    if not A: return False
    for x in A:
        if not contains(R, x): return False
    for x in A:
        for y in A:
            try:
                if not contains(A, x + y): return False
                if not contains(A, x * y): return False
            except Exception:
                return False
    zero = get_zero(R)
    if zero is None or not contains(A, zero): return False
    for x in A:
        inv = None
        for y in R:
            try:
                if bool(x + y == zero):
                    inv = y
                    break
            except Exception:
                pass
        if inv is None or not contains(A, inv): return False
    one = get_one(R)
    if one is not None:
        if not contains(A, one): return False
    return True

def conditions(witness):
    try:
        R = list(witness.R)
        S = list(witness.S)
        f = witness.f
        A = list(witness.A)
    except Exception:
        return [False, False, False]

    # H1: f is a ring homomorphism from R to S
    try:
        h1 = is_ring(R) and is_ring(S) and is_homomorphism(f, R, S)
    except Exception:
        h1 = False

    # H2: A is a subring of R
    try:
        h2 = is_subring(A, R)
    except Exception:
        h2 = False

    # neg_Q: f(A) is NOT a subring of S
    try:
        f_A = []
        for x in A:
            fx = apply_f(f, x)
            if not contains(f_A, fx):
                f_A.append(fx)
        neg_q = not is_subring(f_A, S)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: A is a subring of R",
    "¬Q: The image f(A) is not a subring of S"
]

N_HYP = 2
NEG_Q_INDEX = 2
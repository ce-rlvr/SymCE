import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
SymmetricGroup = sympy.combinatorics.named_groups.SymmetricGroup
AlternatingGroup = sympy.combinatorics.named_groups.AlternatingGroup
DihedralGroup = sympy.combinatorics.named_groups.DihedralGroup
CyclicGroup = sympy.combinatorics.named_groups.CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "H_3: I + J = R",
    "¬Q: I^m + J^n != R"
]

N_HYP = 3
NEG_Q_INDEX = 3

# Helper functions for finite rings
def contains(lst, item):
    for x in lst:
        if x == item:
            return True
    return False

def unique(lst):
    res = []
    for x in lst:
        if not contains(res, x):
            res.append(x)
    return res

def is_subset(sub, lst):
    for x in sub:
        if not contains(lst, x):
            return False
    return True

def same_set(lst1, lst2):
    return is_subset(lst1, lst2) and is_subset(lst2, lst1)

def add_sets(A, B):
    res = []
    for a in A:
        for b in B:
            res.append(a + b)
    return unique(res)

def mul_sets(A, B):
    res = []
    for a in A:
        for b in B:
            res.append(a * b)
    return unique(res)

def get_zero(R):
    for z in R:
        if all(contains(R, a + z) and (a + z == a) for a in R) and \
           all(contains(R, z + a) and (z + a == a) for a in R):
            return z
    return None

def is_commutative_ring(R):
    if not R: return False
    # check closure and commutativity
    for a in R:
        for b in R:
            if not contains(R, a + b): return False
            if not contains(R, a * b): return False
            if a + b != b + a: return False
            if a * b != b * a: return False
    z = get_zero(R)
    if z is None: return False
    # check additive inverse
    for a in R:
        if not any(a + b == z for b in R): return False
    # check associativity and distributivity
    for a in R:
        for b in R:
            for c in R:
                if (a + b) + c != a + (b + c): return False
                if (a * b) * c != a * (b * c): return False
                if a * (b + c) != (a * b) + (a * c): return False
                if (a + b) * c != (a * c) + (b * c): return False
    return True

def is_ideal(I, R):
    if not I: return False
    if not is_subset(I, R): return False
    for a in I:
        for b in I:
            if not contains(I, a + b): return False
    for r in R:
        for a in I:
            if not contains(I, r * a): return False
            if not contains(I, a * r): return False
    z = get_zero(R)
    if not contains(I, z): return False
    for a in I:
        if not any(a + b == z and contains(I, b) for b in I): return False
    return True

def additive_closure(A, R):
    closure = unique(A)
    added = True
    iters = 0
    while added and iters < len(R):
        added = False
        new_elements = []
        for a in closure:
            for b in closure:
                c = a + b
                if not contains(closure, c) and not contains(new_elements, c):
                    new_elements.append(c)
                    added = True
        closure.extend(new_elements)
        iters += 1
    return closure

def ideal_power(I, m, R):
    if m <= 0:
        raise ValueError("Power must be positive")
    prod = unique(I)
    for _ in range(m - 1):
        prod = mul_sets(prod, unique(I))
    return additive_closure(prod, R)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            I = witness['I']
            J = witness['J']
            m = witness['m']
            n = witness['n']
        elif hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
            J = witness.J
            m = witness.m
            n = witness.n
        else:
            R, I, J, m, n = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_commutative_ring(R)
    except Exception:
        h1 = False

    try:
        h2 = is_ideal(I, R) and is_ideal(J, R)
    except Exception:
        h2 = False

    try:
        h3 = same_set(add_sets(I, J), R)
    except Exception:
        h3 = False

    try:
        m = int(m)
        n = int(n)
        Im = ideal_power(I, m, R)
        Jn = ideal_power(J, n, R)
        Im_Jn = add_sets(Im, Jn)
        neg_q = not same_set(Im_Jn, R)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]
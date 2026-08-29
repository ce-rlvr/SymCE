import itertools
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def contains(lst, item):
    for x in lst:
        if x == item:
            return True
    return False

def unique_len(lst):
    unique = []
    for item in lst:
        if not contains(unique, item):
            unique.append(item)
    return len(unique)

def is_subset(A, B):
    for a in A:
        if not contains(B, a):
            return False
    return True

def is_ideal(I, R):
    if not I: return False
    if not is_subset(I, R): return False
    for a in I:
        for b in I:
            try:
                diff = a - b
            except Exception:
                return False
            if not contains(I, diff): return False
    for m in I:
        for r in R:
            try:
                p1 = r * m
                p2 = m * r
            except Exception:
                return False
            if not contains(I, p1): return False
            if not contains(I, p2): return False
    return True

def is_ring(R):
    if not R: return False
    for a in R:
        for b in R:
            try:
                diff = a - b
                prod = a * b
            except Exception:
                return False
            if not contains(R, diff): return False
            if not contains(R, prod): return False
    return True

def generated_ideal(y, R):
    I = [y]
    changed = True
    while changed:
        changed = False
        new_elements = []
        for a in I:
            for b in I:
                try:
                    diff = a - b
                except Exception:
                    continue
                if not contains(I, diff) and not contains(new_elements, diff):
                    new_elements.append(diff)
            for r in R:
                try:
                    p1 = r * a
                    p2 = a * r
                except Exception:
                    continue
                if not contains(I, p1) and not contains(new_elements, p1):
                    new_elements.append(p1)
                if not contains(I, p2) and not contains(new_elements, p2):
                    new_elements.append(p2)
        if new_elements:
            I.extend(new_elements)
            changed = True
    return I

def get_identity(R):
    for e in R:
        is_id = True
        for r in R:
            try:
                if not (e * r == r) or not (r * e == r):
                    is_id = False
                    break
            except Exception:
                is_id = False
                break
        if is_id:
            return e
    return None

def is_unit(x, R):
    e = get_identity(R)
    if e is None:
        return False
    for y in R:
        try:
            if (x * y == e) and (y * x == e):
                return True
        except Exception:
            pass
    return False

def conditions(witness) -> list[bool]:
    try:
        R, M, x = witness
    except Exception:
        return [False, False, False]
    
    # H1: M is the unique maximal ideal of R
    try:
        h1 = False
        if is_ring(R) and is_ideal(M, R) and unique_len(M) < unique_len(R):
            h1 = True
            for y in R:
                if not contains(M, y):
                    I_y = generated_ideal(y, R)
                    if unique_len(I_y) < unique_len(R):
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: x is an element of R that is not contained in M
    try:
        h2 = contains(R, x) and not contains(M, x)
    except Exception:
        h2 = False

    # neg_Q: x is NOT a unit in R
    try:
        neg_q = not is_unit(x, R)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is the unique maximal ideal of R",
    "H_2: x is an element of R that is not contained in M",
    "¬Q: x is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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

def contains(S, x):
    for s in S:
        if s == x:
            return True
    return False

def center(R):
    Z = []
    for x in R:
        is_center = True
        for y in R:
            if not (x * y == y * x):
                is_center = False
                break
        if is_center:
            Z.append(x)
    return Z

def identity(S):
    for e in S:
        is_id = True
        for x in S:
            if not (e * x == x and x * e == x):
                is_id = False
                break
        if is_id:
            return e
    return None

def is_unit(S, u):
    if not contains(S, u):
        return False
    e = identity(S)
    if e is None:
        return False
    for v in S:
        if u * v == e and v * u == e:
            return True
    return False

def conditions(witness):
    try:
        R, u = witness
    except Exception:
        return [False, False, False]
    
    try:
        R = list(R)
        if len(R) == 0 or len(R) > 100:
            h1 = False
        else:
            h1 = True
            for a in R:
                for b in R:
                    if not contains(R, a + b): h1 = False; break
                    if not contains(R, a - b): h1 = False; break
                    if not contains(R, a * b): h1 = False; break
                    if a + b != b + a: h1 = False; break
                if not h1: break
            
            if h1:
                for a in R:
                    for b in R:
                        for c in R:
                            if (a + b) + c != a + (b + c): h1 = False; break
                            if (a * b) * c != a * (b * c): h1 = False; break
                            if a * (b + c) != a * b + a * c: h1 = False; break
                            if (a + b) * c != a * c + b * c: h1 = False; break
                        if not h1: break
                    if not h1: break
    except Exception:
        h1 = False

    try:
        Z = center(R)
        h2 = contains(Z, u)
    except Exception:
        h2 = False

    try:
        unit_in_Z = is_unit(Z, u)
        unit_in_R = is_unit(R, u)
        neg_q = (unit_in_Z != unit_in_R)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: u is an element of Z(R)",
    "¬Q: u is a unit in Z(R) iff u is a unit in R is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2
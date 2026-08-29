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

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def get_d(witness):
    if isinstance(witness, (tuple, list)):
        for item in witness:
            d = get_d(item)
            if d is not None:
                return d
        return None

    try:
        return int(witness)
    except Exception:
        pass

    try:
        sq = witness**2
        return int(sq)
    except Exception:
        pass

    try:
        s = str(witness).replace(' ', '')
        if 'sqrt(' in s:
            start = s.find('sqrt(') + 5
            end = s.find(')', start)
            if end != -1:
                return int(s[start:end])
    except Exception:
        pass

    return None

def is_valid_d(d):
    if d == 0 or d == 1:
        return False
    factors = sympy.factorint(abs(d))
    return all(v == 1 for v in factors.values())

def is_euclidean(d):
    if d < 0:
        return d in {-1, -2, -3, -7, -11}
    else:
        known_euclidean = {2, 3, 5, 6, 7, 11, 13, 14, 17, 19, 21, 29, 33, 37, 41, 57, 69, 73}
        return d in known_euclidean

def conditions(witness) -> list[bool]:
    d = get_d(witness)
    
    try:
        if d is not None:
            h1 = is_valid_d(d)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if d is not None:
            neg_q = not is_euclidean(d)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: O_K is the ring of integers of K",
    "¬Q: O_K is not a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1
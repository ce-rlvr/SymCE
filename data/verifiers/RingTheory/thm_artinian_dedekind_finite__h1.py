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

def _is_identity(x, one):
    try:
        if x is one: 
            return True
    except Exception: 
        pass
    try:
        eq = (x == one)
        if isinstance(eq, bool) and eq: 
            return True
        if bool(eq): 
            return True
    except Exception: 
        pass
    try:
        eq = (x == 1)
        if isinstance(eq, bool) and eq: 
            return True
        if bool(eq): 
            return True
    except Exception: 
        pass
    try:
        if getattr(x, 'is_Identity', False): 
            return True
    except Exception: 
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, a, b = witness
            one = getattr(R, 'one', 1)
        elif isinstance(witness, tuple) and len(witness) == 2:
            a, b = witness
            one = 1
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1_ok = _is_identity(a * b, one)
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = not _is_identity(b * a, one)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a and b are elements of R such that ab = 1",
    "¬Q: ba != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
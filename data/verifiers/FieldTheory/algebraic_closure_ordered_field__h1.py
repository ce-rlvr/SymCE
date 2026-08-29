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

QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def is_field(F):
    try:
        if F in (QQ, RR, CC):
            return True
        if hasattr(F, 'is_Field'):
            return bool(F.is_Field)
        return False
    except Exception:
        return False

def is_ordered_field(F):
    try:
        if not is_field(F):
            return False
        if F == CC:
            return False
        if hasattr(F, 'characteristic'):
            char = F.characteristic() if callable(F.characteristic) else F.characteristic
            if char != 0:
                return False
        if hasattr(F, 'ext'):
            ext = F.ext
            if hasattr(ext, 'is_real') and ext.is_real is False:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        h1 = is_ordered_field(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = is_field(witness)
    except Exception:
        h2 = False
        
    try:
        neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is an ordered field",
    "H_2: Fbar is the algebraic closure of F",
    "not Q: Fbar can be equipped with a strict total order that makes it an ordered field"
]

N_HYP = 2
NEG_Q_INDEX = 2
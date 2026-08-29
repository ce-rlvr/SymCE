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

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, a, b = witness
        else:
            R = witness.R
            a = witness.a
            b = witness.b
    except Exception:
        return [False, False]
    
    try:
        if callable(R.is_UFD):
            h1 = bool(R.is_UFD())
        else:
            h1 = bool(R.is_UFD)
    except Exception:
        h1 = False
        
    try:
        if hasattr(R, 'has_gcd'):
            neg_q = not bool(R.has_gcd(a, b))
        elif hasattr(R, 'gcd'):
            d = R.gcd(a, b)
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: a and b do not have a greatest common divisor in R"
]

N_HYP = 1
NEG_Q_INDEX = 1
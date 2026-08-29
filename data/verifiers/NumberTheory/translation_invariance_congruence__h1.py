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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            m = witness.get('m')
        else:
            a, b, c, m = witness
    except Exception:
        return [False, False, False]

    def is_int(x):
        if isinstance(x, int):
            return True
        if hasattr(x, 'is_integer'):
            val = x.is_integer() if callable(x.is_integer) else x.is_integer
            if val is True:
                return True
        return False

    # H_1: m is a positive integer
    try:
        h1 = is_int(m) and m > 0
    except Exception:
        h1 = False

    # H_2: a \equiv b \pmod m
    try:
        h2 = is_int(a) and is_int(b) and (a - b) % m == 0
    except Exception:
        h2 = False

    # Q: a + c \equiv b + c \pmod m
    try:
        val1 = a + c
        val2 = b + c
        # Congruence modulo m is defined over integers.
        # If c is not an integer, a+c and b+c will not be integers,
        # making the congruence undefined (i.e., the conclusion fails).
        q = is_int(val1) and is_int(val2) and (val1 - val2) % m == 0
    except Exception:
        q = False

    return [bool(h1), bool(h2), not bool(q)]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: a \\equiv b \\pmod m",
    "¬Q: a + c \\not\\equiv b + c \\pmod m"
]

N_HYP = 2
NEG_Q_INDEX = 2
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

# Standard algebra objects
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

def is_integer_val(x):
    if isinstance(x, int):
        return True
    if isinstance(x, float):
        return x.is_integer()
    if isinstance(x, complex):
        return x.imag == 0 and float(x.real).is_integer()
    if isinstance(x, sympy.Rational):
        return x.q == 1
    if isinstance(x, sympy.Integer):
        return True
    if hasattr(x, 'is_integer') and x.is_integer is not None:
        return bool(x.is_integer)
    try:
        return int(x) == x
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            return [False]
        if type(witness).__module__.startswith('sympy.combinatorics'):
            return [False]
        if isinstance(witness, str):
            return [False]
        if isinstance(witness, sympy.Expr) and not witness.is_number:
            return [False]
        _ = witness + 0
    except Exception:
        return [False]

    try:
        is_int = is_integer_val(witness)
    except Exception:
        is_int = False

    try:
        if is_int:
            if isinstance(witness, complex):
                val = int(witness.real)
            else:
                val = int(witness)
            lhs = (val % 4 != 2)
        else:
            lhs = False
    except Exception:
        lhs = False

    try:
        if is_int:
            if isinstance(witness, complex):
                val = int(witness.real)
            else:
                val = int(witness)
            rhs_val = (val % 4 != 2)
        else:
            rhs_val = True
    except Exception:
        rhs_val = False

    try:
        neg_q = (lhs != rhs_val)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The equivalence (exists x, y in Z: x^2 - y^2 = n) <==> (n % 4 != 2) fails"
]

N_HYP = 0
NEG_Q_INDEX = 0
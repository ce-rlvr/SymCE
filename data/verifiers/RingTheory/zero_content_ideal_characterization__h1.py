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

CONDITION_LABELS = ["H_1: f is a polynomial in the polynomial ring R", "not Q: The content ideal c(f) is the zero ideal if and only if f is the zero polynomial fails"]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    try:
        if hasattr(witness, 'is_polynomial_in_Rx'):
            val = witness.is_polynomial_in_Rx
            h1 = bool(val()) if callable(val) else bool(val)
        elif hasattr(witness, 'is_polynomial'):
            val = witness.is_polynomial
            h1 = bool(val()) if callable(val) else bool(val)
        elif hasattr(witness, 'is_poly'):
            val = witness.is_poly
            h1 = bool(val()) if callable(val) else bool(val)
        elif isinstance(witness, sympy.Poly):
            h1 = True
    except Exception:
        h1 = False

    neg_q = False
    try:
        c_zero = None
        if hasattr(witness, 'content_ideal_is_zero'):
            val = witness.content_ideal_is_zero
            c_zero = bool(val()) if callable(val) else bool(val)
        elif hasattr(witness, 'c_is_zero'):
            val = witness.c_is_zero
            c_zero = bool(val()) if callable(val) else bool(val)
        elif hasattr(witness, 'content_is_zero'):
            val = witness.content_is_zero
            c_zero = bool(val()) if callable(val) else bool(val)
        elif hasattr(witness, 'content'):
            val = witness.content
            c = val() if callable(val) else val
            c_zero = (c == 0)

        f_zero = None
        if hasattr(witness, 'is_zero_polynomial'):
            val = witness.is_zero_polynomial
            f_zero = bool(val()) if callable(val) else bool(val)
        elif hasattr(witness, 'is_zero_poly'):
            val = witness.is_zero_poly
            f_zero = bool(val()) if callable(val) else bool(val)
        elif hasattr(witness, 'is_zero'):
            val = witness.is_zero
            f_zero = bool(val()) if callable(val) else bool(val)
        elif isinstance(witness, sympy.Poly):
            f_zero = witness.is_zero

        if c_zero is not None and f_zero is not None:
            neg_q = (c_zero != f_zero)
    except Exception:
        neg_q = False

    return [h1, neg_q]
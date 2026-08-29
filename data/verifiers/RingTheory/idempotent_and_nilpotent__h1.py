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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_zero(e):
    try:
        if hasattr(e, 'is_zero_matrix'):
            val = e.is_zero_matrix
            if callable(val):
                val = val()
            if val is True:
                return True
    except Exception:
        pass
    try:
        from sympy import MatrixBase
        if isinstance(e, MatrixBase):
            for i in range(e.rows):
                for j in range(e.cols):
                    if not is_zero(e[i, j]):
                        return False
            return True
    except Exception:
        pass
    try:
        if hasattr(e, 'is_zero'):
            val = e.is_zero
            if callable(val):
                val = val()
            if val is True:
                return True
    except Exception:
        pass
    try:
        if hasattr(e, 'equals'):
            res = e.equals(0)
            if res is True:
                return True
    except Exception:
        pass
    try:
        eq = (e == 0)
        if hasattr(eq, 'all'):
            if eq.all():
                return True
        elif eq:
            return True
    except Exception:
        pass
    return False

def is_equal(a, b):
    try:
        if is_zero(a - b):
            return True
    except Exception:
        pass
    try:
        eq = (a == b)
        if hasattr(eq, 'all'):
            if eq.all():
                return True
        elif eq:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    h1 = False
    try:
        h1 = is_equal(witness * witness, witness)
    except Exception:
        pass
    if not h1:
        try:
            h1 = is_equal(witness**2, witness)
        except Exception:
            pass

    h2 = False
    try:
        curr = witness
        for n in range(1, 100):
            if is_zero(curr):
                h2 = True
                break
            curr = curr * witness
    except Exception:
        pass
    
    if not h2:
        try:
            for n in range(1, 100):
                if is_zero(witness**n):
                    h2 = True
                    break
        except Exception:
            pass

    neg_q = False
    try:
        neg_q = not is_zero(witness)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: e is an idempotent element (e^2 = e)",
    "H_2: e is a nilpotent element (e^n = 0 for some n >= 1)",
    "¬Q: e != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2
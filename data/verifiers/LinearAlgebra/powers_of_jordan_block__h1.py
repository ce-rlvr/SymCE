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

def conditions(witness):
    try:
        J, m, lam = witness
        h1 = (isinstance(m, int) or isinstance(m, sympy.Integer)) and m > 0
    except Exception:
        h1 = False

    try:
        J, m, lam = witness
        if not isinstance(J, sympy.MatrixBase):
            q = False
        elif not J.is_square:
            q = False
        else:
            n = J.shape[0]
            J_m = J**m
            q = True
            
            for i in range(n):
                for j in range(i):
                    if sympy.simplify(J_m[i, j]) != 0:
                        q = False
                        break
                if not q:
                    break
            
            if q:
                for i in range(n):
                    for j in range(i, n):
                        diff = j - i
                        if m >= diff:
                            expected = sympy.binomial(m, diff) * (lam ** (m - diff))
                        else:
                            expected = 0
                        if sympy.simplify(J_m[i, j] - expected) != 0:
                            q = False
                            break
                    if not q:
                        break
    except Exception:
        q = False

    neg_q = not q
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "¬Q: J^m is not upper triangular or its entries do not match the expected formula"
]

N_HYP = 1
NEG_Q_INDEX = 1
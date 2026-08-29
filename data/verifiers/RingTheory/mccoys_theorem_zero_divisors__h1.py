import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: f(x) is a zero divisor in the polynomial ring",
    "H_2: f(x) is not the zero polynomial",
    "¬Q: There does not exist a non-zero element c in R such that c f(x) = 0"
]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
        else:
            f, g = witness
            
        if not isinstance(f, (list, tuple)) or not isinstance(g, (list, tuple)):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def is_zero_element(c):
        if hasattr(c, 'is_zero_matrix'):
            return c.is_zero_matrix
        if hasattr(c, 'is_zero') and c.is_zero is not None:
            return c.is_zero
        return c == 0

    def is_zero_poly(p):
        try:
            return all(is_zero_element(c) for c in p)
        except Exception:
            return False

    def poly_mul(p1, p2):
        deg1 = len(p1) - 1
        deg2 = len(p2) - 1
        
        if hasattr(p1[0], 'shape'):
            zero_elem = sympy.zeros(*p1[0].shape)
        else:
            zero_elem = 0
            
        res = [zero_elem for _ in range(deg1 + deg2 + 1)]
        for i in range(deg1 + 1):
            for j in range(deg2 + 1):
                res[i+j] = res[i+j] + p1[i] * p2[j]
        return res

    try:
        g_not_zero = not is_zero_poly(g)
        fg_zero = is_zero_poly(poly_mul(f, g))
        gf_zero = is_zero_poly(poly_mul(g, f))
        h1 = bool(g_not_zero and (fg_zero or gf_zero))
    except Exception:
        h1 = False

    try:
        h2 = bool(not is_zero_poly(f))
    except Exception:
        h2 = False

    try:
        if hasattr(f[0], 'shape'):
            M = sympy.Matrix.hstack(*f)
            n = f[0].shape[0]
            neg_q = bool(M.rank() == n)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
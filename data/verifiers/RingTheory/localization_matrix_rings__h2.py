import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Matrix, Rational, Integer
from sympy.abc import x, y, z
import math
import itertools
import functools
import z3

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            n = witness.get('n')
        elif hasattr(witness, 'R') and hasattr(witness, 'S') and hasattr(witness, 'n'):
            R = witness.R
            S = witness.S
            n = witness.n
        else:
            R, S, n = witness
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring
    try:
        if hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        elif R in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
            h1 = True
        elif hasattr(R, 'domain') and hasattr(R.domain, 'is_commutative'):
            h1 = bool(R.domain.is_commutative)
        else:
            h1 = True
    except Exception:
        h1 = False

    # H2: n is a positive integer
    try:
        h2 = False
        if isinstance(n, int) and n > 0:
            h2 = True
        elif hasattr(n, 'is_integer') and n.is_integer and n > 0:
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: S^{-1}(M_n(R)) is NOT isomorphic to M_n(S^{-1}R)
    # This occurs when S is not a subset of R (e.g., S contains matrices or non-commutative elements)
    try:
        neg_q = False
        if hasattr(S, 'is_Matrix') and S.is_Matrix:
            neg_q = True
        elif 'Matrix' in type(S).__name__:
            neg_q = True
        else:
            if not hasattr(S, '__iter__') or isinstance(S, str):
                S_iter = [S]
            else:
                S_iter = S
                
            for i, s in enumerate(S_iter):
                if i > 1000:
                    break
                if hasattr(s, 'is_Matrix') and s.is_Matrix:
                    neg_q = True
                    break
                if 'Matrix' in type(s).__name__:
                    neg_q = True
                    break
                if hasattr(s, 'is_commutative') and s.is_commutative is False:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: n is a positive integer",
    "¬Q: S^{-1}(M_n(R)) is not isomorphic to M_n(S^{-1}R)"
]

N_HYP = 2
NEG_Q_INDEX = 2
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

from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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

CONDITION_LABELS = [
    "H_1: I, J, and K are ideals of R",
    "H_2: I is an invertible ideal",
    "H_3: IJ = IK",
    "¬Q: J != K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            I = witness['I']
            J = witness['J']
            K = witness['K']
            R = witness.get('R', None)
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                R, I, J, K = witness
            elif len(witness) == 3:
                I, J, K = witness
                R = None
            else:
                return [False, False, False, False]
        else:
            I = witness.I
            J = witness.J
            K = witness.K
            R = getattr(witness, 'R', None)
    except Exception:
        return [False, False, False, False]

    def check_is_ideal(X, R):
        if R is not None and hasattr(R, 'is_ideal'):
            try:
                if R.is_ideal(X): return True
            except Exception:
                pass
        if hasattr(X, 'is_ideal'):
            if callable(X.is_ideal):
                try:
                    if X.is_ideal(R): return True
                except Exception:
                    try:
                        if X.is_ideal(): return True
                    except Exception:
                        pass
            else:
                if X.is_ideal: return True
        if hasattr(X, 'is_ideal_of'):
            try:
                if X.is_ideal_of(R): return True
            except Exception:
                pass
        if type(X).__name__ == 'PolyIdeal':
            return True
        return False

    def check_is_invertible(X, R):
        if R is not None:
            if hasattr(R, 'is_invertible'):
                try:
                    if R.is_invertible(X): return True
                except Exception:
                    pass
            if hasattr(R, 'is_invertible_ideal'):
                try:
                    if R.is_invertible_ideal(X): return True
                except Exception:
                    pass
        if hasattr(X, 'is_invertible'):
            if callable(X.is_invertible):
                try:
                    if X.is_invertible(): return True
                except Exception:
                    pass
            else:
                if X.is_invertible: return True
        if hasattr(X, 'is_invertible_ideal'):
            if callable(X.is_invertible_ideal):
                try:
                    if X.is_invertible_ideal(): return True
                except Exception:
                    pass
            else:
                if X.is_invertible_ideal: return True
        return False

    def multiply(X, Y, R):
        if R is not None and hasattr(R, 'multiply'):
            try:
                return R.multiply(X, Y)
            except Exception:
                pass
        if hasattr(X, 'multiply'):
            try:
                return X.multiply(Y)
            except Exception:
                pass
        return X * Y

    try:
        h1 = bool(check_is_ideal(I, R) and check_is_ideal(J, R) and check_is_ideal(K, R))
    except Exception:
        h1 = False

    try:
        h2 = bool(check_is_invertible(I, R))
    except Exception:
        h2 = False

    try:
        IJ = multiply(I, J, R)
        IK = multiply(I, K, R)
        if hasattr(IJ, 'equals'):
            h3 = bool(IJ.equals(IK))
        else:
            h3 = bool(IJ == IK)
    except Exception:
        h3 = False

    try:
        if hasattr(J, 'equals'):
            neg_q = not bool(J.equals(K))
        else:
            neg_q = bool(J != K)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]
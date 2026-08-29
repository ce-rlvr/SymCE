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

# Top-level setup for standard algebra objects
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

def conditions(witness) -> list[bool]:
    # The witness could be a tuple (V, T) or just T.
    if isinstance(witness, tuple) and len(witness) == 2:
        V, T = witness
    else:
        V, T = None, witness

    # H_1: V is a finite-dimensional vector space over a field F
    h1 = False
    try:
        if V is not None:
            if isinstance(V, int) and V >= 0:
                h1 = True
            elif hasattr(V, 'dimension'):
                h1 = V.dimension >= 0
            elif hasattr(V, 'shape'):
                h1 = True
            else:
                h1 = True  # Accept mock V
        else:
            if hasattr(T, 'shape'):
                h1 = len(T.shape) == 2
            elif hasattr(T, 'is_diagonalizable'):
                h1 = True
            else:
                h1 = False
    except Exception:
        h1 = False

    # ¬Q: T is diagonalizable if and only if T* is diagonalizable is FALSE
    neg_q = False
    try:
        t_diag_attr = T.is_diagonalizable
        t_diag = bool(t_diag_attr() if callable(t_diag_attr) else t_diag_attr)
        
        # Determine T* (dual operator / adjoint / transpose)
        if hasattr(T, 'dual'):
            T_star = T.dual() if callable(T.dual) else T.dual
        elif hasattr(T, 'T'):
            T_star = T.T() if callable(T.T) else T.T
        elif hasattr(T, 'transpose'):
            T_star = T.transpose() if callable(T.transpose) else T.transpose
        elif hasattr(T, 'adjoint'):
            T_star = T.adjoint() if callable(T.adjoint) else T.adjoint
        else:
            T_star = None
            
        if T_star is not None:
            t_star_diag_attr = T_star.is_diagonalizable
            t_star_diag = bool(t_star_diag_attr() if callable(t_star_diag_attr) else t_star_diag_attr)
            
            # The conclusion is that they are equivalent. We want the negation.
            q = (t_diag == t_star_diag)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "¬Q: T is diagonalizable if and only if T* is diagonalizable is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1
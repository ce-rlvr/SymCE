import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
from sympy.polys import ZZ, QQ
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('R_is_PID', False) and witness.get('K_is_frac_field', False))
        else:
            R, K, L, S = witness
            h1 = bool(getattr(R, 'is_PID', False) and K == R.get_field())
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('L_is_finite_separable_ext', False))
        else:
            R, K, L, S = witness
            h2 = bool(hasattr(L, 'ext') and L.domain == K)
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            neg_q = not bool(witness.get('S_is_Dedekind', True))
        else:
            R, K, L, S = witness
            is_dedekind = getattr(S, 'is_Dedekind', getattr(S, 'is_PID', True))
            neg_q = not bool(is_dedekind)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain with field of fractions K",
    "H_2: L is a finite separable field extension of K",
    "¬Q: S is not a Dedekind domain"
]

N_HYP = 2
NEG_Q_INDEX = 2
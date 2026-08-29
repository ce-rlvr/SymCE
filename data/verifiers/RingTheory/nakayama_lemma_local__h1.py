import math
import itertools
import functools
import z3
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
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
    h1 = False
    h2 = False
    h3 = False
    neg_q = False

    if callable(witness):
        try:
            res = witness()
            if isinstance(res, (list, tuple)) and len(res) == 4:
                return [bool(x) for x in res]
        except Exception:
            pass

    # H1: R is a local ring with maximal ideal m
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_local_ring', witness.get('R_is_local', witness.get('H1', False))))
        elif hasattr(witness, 'is_local_ring'):
            val = witness.is_local_ring
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'R') and hasattr(witness.R, 'is_local_ring'):
            val = witness.R.is_local_ring
            h1 = bool(val() if callable(val) else val)
        elif isinstance(witness, tuple) and len(witness) >= 1:
            if hasattr(witness[0], 'is_local_ring'):
                val = witness[0].is_local_ring
                h1 = bool(val() if callable(val) else val)
    except Exception:
        pass

    # H2: M is a finitely generated R-module
    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('is_finitely_generated', witness.get('M_is_fg', witness.get('H2', False))))
        elif hasattr(witness, 'is_finitely_generated'):
            val = witness.is_finitely_generated
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'M') and hasattr(witness.M, 'is_finitely_generated'):
            val = witness.M.is_finitely_generated
            h2 = bool(val() if callable(val) else val)
        elif isinstance(witness, tuple) and len(witness) >= 3:
            if hasattr(witness[2], 'is_finitely_generated'):
                val = witness[2].is_finitely_generated
                h2 = bool(val() if callable(val) else val)
    except Exception:
        pass

    # H3: mM = M
    try:
        if isinstance(witness, dict):
            h3 = bool(witness.get('mM_equals_M', witness.get('mM_eq_M', witness.get('H3', False))))
        elif hasattr(witness, 'mM_equals_M'):
            val = witness.mM_equals_M
            h3 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'mM_eq_M'):
            val = witness.mM_eq_M
            h3 = bool(val() if callable(val) else val)
        elif isinstance(witness, tuple) and len(witness) >= 3:
            m = witness[1]
            M = witness[2]
            if hasattr(m, '__mul__'):
                h3 = (m * M == M)
    except Exception:
        pass

    # ¬Q: M is not the zero module
    try:
        if isinstance(witness, dict):
            neg_q = not bool(witness.get('is_zero_module', witness.get('M_is_zero', witness.get('Q', True))))
        elif hasattr(witness, 'is_zero_module'):
            val = witness.is_zero_module
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, 'M') and hasattr(witness.M, 'is_zero'):
            val = witness.M.is_zero
            neg_q = not bool(val() if callable(val) else val)
        elif isinstance(witness, tuple) and len(witness) >= 3:
            if hasattr(witness[2], 'is_zero'):
                val = witness[2].is_zero
                neg_q = not bool(val() if callable(val) else val)
            elif hasattr(witness[2], 'is_zero_module'):
                val = witness[2].is_zero_module
                neg_q = not bool(val() if callable(val) else val)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a local ring with maximal ideal m",
    "H_2: M is a finitely generated R-module",
    "H_3: mM = M",
    "¬Q: M is not the zero module"
]

N_HYP = 3
NEG_Q_INDEX = 3
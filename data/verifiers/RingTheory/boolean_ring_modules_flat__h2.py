import sympy
from sympy import *
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
    h1 = False
    neg_q = False
    
    try:
        w = witness
        if callable(w) and not isinstance(w, type):
            try:
                w = w()
            except Exception:
                pass
                
        # Check H1: R is a Boolean ring
        if isinstance(w, dict):
            if 'is_boolean_ring' in w:
                h1 = bool(w['is_boolean_ring'])
            elif 'R_is_boolean' in w:
                h1 = bool(w['R_is_boolean'])
        elif hasattr(w, 'is_boolean_ring'):
            val = w.is_boolean_ring
            h1 = bool(val() if callable(val) else val)
        elif hasattr(w, 'is_BooleanRing'):
            val = w.is_BooleanRing
            h1 = bool(val() if callable(val) else val)
        elif hasattr(w, 'R') and hasattr(w.R, 'is_boolean_ring'):
            val = w.R.is_boolean_ring
            h1 = bool(val() if callable(val) else val)
        elif isinstance(w, tuple) and len(w) == 2:
            R, M = w
            if hasattr(R, 'is_boolean_ring'):
                val = R.is_boolean_ring
                h1 = bool(val() if callable(val) else val)
            elif hasattr(R, 'is_boolean'):
                val = R.is_boolean
                h1 = bool(val() if callable(val) else val)
        elif isinstance(w, str):
            if 'boolean ring' in w.lower():
                h1 = True
    except Exception:
        pass

    try:
        w = witness
        if callable(w) and not isinstance(w, type):
            try:
                w = w()
            except Exception:
                pass

        is_flat = True
        if isinstance(w, dict):
            if 'is_flat_module' in w:
                is_flat = bool(w['is_flat_module'])
            elif 'M_is_flat' in w:
                is_flat = bool(w['M_is_flat'])
            elif 'is_flat' in w:
                is_flat = bool(w['is_flat'])
        elif hasattr(w, 'is_flat_module'):
            val = w.is_flat_module
            is_flat = bool(val() if callable(val) else val)
        elif hasattr(w, 'is_FlatModule'):
            val = w.is_FlatModule
            is_flat = bool(val() if callable(val) else val)
        elif hasattr(w, 'M') and hasattr(w.M, 'is_flat_module'):
            val = w.M.is_flat_module
            is_flat = bool(val() if callable(val) else val)
        elif hasattr(w, 'M') and hasattr(w.M, 'is_flat'):
            val = w.M.is_flat
            is_flat = bool(val() if callable(val) else val)
        elif isinstance(w, tuple) and len(w) == 2:
            R, M = w
            if hasattr(M, 'is_flat_module'):
                val = M.is_flat_module
                is_flat = bool(val() if callable(val) else val)
            elif hasattr(M, 'is_flat'):
                val = M.is_flat
                is_flat = bool(val() if callable(val) else val)
        elif isinstance(w, str):
            w_lower = w.lower()
            if 'not flat' in w_lower or 'non-flat' in w_lower or "isn't flat" in w_lower or 'fails to be flat' in w_lower:
                is_flat = False

        neg_q = not is_flat
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: M is not a flat R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1
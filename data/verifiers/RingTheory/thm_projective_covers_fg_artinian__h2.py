import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
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

def extract_bool(obj, keys, default):
    if isinstance(obj, dict):
        for k in keys:
            if k in obj:
                return bool(obj[k])
    else:
        for k in keys:
            if hasattr(obj, k):
                val = getattr(obj, k)
                if callable(val):
                    try:
                        val = val()
                    except Exception:
                        continue
                return bool(val)
    return default

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            s = witness.lower()
            h1 = "right artinian" in s
            neg_q = ("no projective cover" in s or 
                     "does not have a projective cover" in s or 
                     "without a projective cover" in s or 
                     "not have a projective cover" in s)
            return [h1, neg_q]
            
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
            h1 = extract_bool(R, ['is_right_Artinian', 'right_artinian', 'is_right_artinian'], False)
            has_proj = extract_bool(M, ['has_projective_cover', 'projective_cover', 'is_projective_cover'], True)
            neg_q = not has_proj
        else:
            h1 = extract_bool(witness, ['is_right_Artinian', 'right_artinian', 'is_right_artinian'], False)
            has_proj = extract_bool(witness, ['has_projective_cover', 'projective_cover', 'is_projective_cover'], True)
            neg_q = not has_proj
            
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: M does not have a projective cover"
]

N_HYP = 1
NEG_Q_INDEX = 1
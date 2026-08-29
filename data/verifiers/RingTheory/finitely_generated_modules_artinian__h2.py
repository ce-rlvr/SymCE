import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

def check_prop(obj, prop_names, default=False):
    if isinstance(obj, dict):
        for p in prop_names:
            if p in obj:
                return bool(obj[p])
    else:
        for p in prop_names:
            if hasattr(obj, p):
                val = getattr(obj, p)
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        pass
                else:
                    return bool(val)
    return default

def conditions(witness) -> list[bool]:
    h1 = h2 = h3 = h4 = neg_q = False
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
            h1 = check_prop(R, ['is_ring', 'R_is_ring'])
            h2 = check_prop(R, ['is_left_artinian', 'is_artinian', 'R_is_left_artinian'])
            
            if hasattr(M, 'is_left_module') and callable(M.is_left_module):
                try:
                    h3 = bool(M.is_left_module(R))
                except Exception:
                    h3 = check_prop(M, ['is_left_module', 'M_is_left_module'])
            else:
                h3 = check_prop(M, ['is_left_module', 'M_is_left_module'])
                
            h4 = check_prop(M, ['is_finitely_generated', 'M_is_finitely_generated'])
            
            m_art = check_prop(M, ['is_artinian', 'M_is_artinian'], default=True)
            neg_q = not m_art
        else:
            h1 = check_prop(witness, ['R_is_ring', 'is_ring'])
            h2 = check_prop(witness, ['R_is_left_artinian', 'is_left_artinian'])
            h3 = check_prop(witness, ['M_is_left_R_module', 'M_is_left_module', 'is_left_module'])
            h4 = check_prop(witness, ['M_is_finitely_generated', 'is_finitely_generated'])
            
            m_art = check_prop(witness, ['M_is_artinian', 'is_artinian'], default=True)
            neg_q = not m_art
    except Exception:
        pass

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R is a left Artinian ring",
    "H_3: M is a left R-module",
    "H_4: M is finitely generated",
    "¬Q: M is not an Artinian module"
]

N_HYP = 4
NEG_Q_INDEX = 4
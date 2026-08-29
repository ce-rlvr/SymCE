import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

def _check_prop(obj, prop_names):
    if isinstance(obj, dict):
        for p in prop_names:
            if p in obj:
                val = obj[p]
                return bool(val() if callable(val) else val)
    for p in prop_names:
        if hasattr(obj, p):
            val = getattr(obj, p)
            return bool(val() if callable(val) else val)
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
            h1 = _check_prop(R, ['is_right_artinian', 'right_artinian', 'R_is_right_artinian', 'R_right_artinian'])
            m_art = _check_prop(M, ['is_artinian', 'artinian', 'M_is_artinian', 'M_artinian'])
            m_noe = _check_prop(M, ['is_noetherian', 'noetherian', 'M_is_noetherian', 'M_noetherian'])
        else:
            h1 = _check_prop(witness, ['is_right_artinian', 'right_artinian', 'R_is_right_artinian', 'R_right_artinian'])
            m_art = _check_prop(witness, ['is_artinian', 'artinian', 'M_is_artinian', 'M_artinian'])
            m_noe = _check_prop(witness, ['is_noetherian', 'noetherian', 'M_is_noetherian', 'M_noetherian'])
            
        neg_q = (bool(m_art) != bool(m_noe))
        
        return [bool(h1), neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: M is Artinian XOR M is Noetherian (conclusion fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy import CC, QQ, RR, ZZ, GF
from sympy.abc import x, y, z
import re

# Top-level setup for FieldTheory
# Standard fields are already imported from sympy

def is_algebraically_closed(K):
    if hasattr(K, 'is_algebraically_closed'):
        val = K.is_algebraically_closed
        if callable(val):
            return val()
        return bool(val)
    s = str(K)
    if s in ['CC', 'Complexes', 'ComplexField', 'C']:
        return True
    if 'AlgebraicClosure' in s:
        return True
    return False

def is_divisible_multiplicative_group(K):
    if hasattr(K, 'is_divisible_multiplicative_group'):
        val = K.is_divisible_multiplicative_group
        if callable(val):
            return val()
        return bool(val)
    s = str(K)
    if s in ['CC', 'Complexes', 'ComplexField', 'C']:
        return True
    if 'AlgebraicClosure' in s:
        return True
    if s in ['RR', 'Reals', 'RealField', 'R', 'QQ', 'Rationals', 'RationalField', 'Q', 'ZZ', 'Integers', 'IntegerRing', 'Z']:
        return False
    if hasattr(K, 'order'):
        try:
            return int(K.order) == 2
        except Exception:
            pass
    if hasattr(K, 'mod'):
        try:
            return int(K.mod) == 2
        except Exception:
            pass
    if s == 'GF(2)':
        return True
    if s.startswith('GF('):
        m = re.match(r'GF\((.+)\)', s)
        if m:
            try:
                p = int(m.group(1))
                return p == 2
            except Exception:
                pass
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = is_algebraically_closed(witness)
    except Exception:
        h1 = False
        
    try:
        q = is_divisible_multiplicative_group(witness)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: K^\\times is not a divisible group"
]

N_HYP = 1
NEG_Q_INDEX = 1
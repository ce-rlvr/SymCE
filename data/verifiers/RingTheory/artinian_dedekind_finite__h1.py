import sympy
from sympy import eye, simplify
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_identity(obj):
    """Helper to check if an object acts as the multiplicative identity."""
    try:
        if obj == 1:
            return True
    except Exception:
        pass
    
    try:
        if getattr(obj, 'is_Identity', False):
            return True
    except Exception:
        pass
        
    try:
        if hasattr(obj, 'is_one') and obj.is_one:
            return True
    except Exception:
        pass
        
    try:
        if hasattr(obj, 'rows') and hasattr(obj, 'cols') and obj.rows == obj.cols:
            if obj == eye(obj.rows):
                return True
    except Exception:
        pass
        
    try:
        if simplify(obj) == 1:
            return True
    except Exception:
        pass
        
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            a, b = witness
        else:
            a, b = witness.a, witness.b
    except Exception:
        try:
            a, b = witness
        except Exception:
            return [False, False]
            
    try:
        ab = a * b
        h1 = is_identity(ab)
    except Exception:
        h1 = False
        
    try:
        ba = b * a
        neg_q = not is_identity(ba)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are elements such that ab = 1",
    "¬Q: ba != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
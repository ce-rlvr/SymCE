import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_finite(F):
    if isinstance(F, (set, list, tuple, frozenset)):
        return True
    if hasattr(F, 'is_finite'):
        val = F.is_finite() if callable(F.is_finite) else F.is_finite
        if val:
            return True
    if hasattr(F, 'order'):
        val = F.order() if callable(F.order) else F.order
        try:
            if float(val) < float('inf'):
                return True
        except Exception:
            pass
    if hasattr(F, 'size'):
        val = F.size() if callable(F.size) else F.size
        try:
            if float(val) < float('inf'):
                return True
        except Exception:
            pass
    if hasattr(F, 'domain') and hasattr(F.domain, 'is_finite'):
        val = F.domain.is_finite() if callable(F.domain.is_finite) else F.domain.is_finite
        if val:
            return True
    return False

def is_algebraically_closed_field(F):
    if F == sympy.CC:
        return True
    
    # Mathematically, no finite field is algebraically closed.
    if is_finite(F):
        return False
        
    if hasattr(F, 'is_algebraically_closed'):
        val = F.is_algebraically_closed() if callable(F.is_algebraically_closed) else F.is_algebraically_closed
        if val:
            return True
            
    return False

def conditions(witness):
    try:
        h1 = bool(is_finite(witness))
    except Exception:
        h1 = False

    try:
        neg_q = bool(is_algebraically_closed_field(witness))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The set of elements in F is finite",
    "¬Q: F is an algebraically closed field"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.matrices import *
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            if 'e1_idemp' in witness and 'e2_idemp' in witness and 'R_idemp' in witness:
                e1_idemp = bool(witness['e1_idemp'])
                e2_idemp = bool(witness['e2_idemp'])
                R_idemp = bool(witness['R_idemp'])
                Q = (R_idemp == (e1_idemp and e2_idemp))
                return [True, True, not Q]
                
            e1 = witness['e1']
            e2 = witness['e2']
            R1_mult = witness.get('R1_mult', lambda x, y: x * y)
            R2_mult = witness.get('R2_mult', lambda x, y: x * y)
            R_mult = witness.get('R_mult', lambda x, y: (R1_mult(x[0], y[0]), R2_mult(x[1], y[1])))
        elif isinstance(witness, tuple) and len(witness) == 3:
            e1_idemp, e2_idemp, R_idemp = witness
            Q = (bool(R_idemp) == (bool(e1_idemp) and bool(e2_idemp)))
            return [True, True, not Q]
        else:
            if hasattr(witness, 'e1_idemp') and hasattr(witness, 'e2_idemp') and hasattr(witness, 'R_idemp'):
                e1_idemp = bool(witness.e1_idemp)
                e2_idemp = bool(witness.e2_idemp)
                R_idemp = bool(witness.R_idemp)
                Q = (R_idemp == (e1_idemp and e2_idemp))
                return [True, True, not Q]
                
            e1 = witness.e1
            e2 = witness.e2
            R1_mult = getattr(witness, 'R1_mult', lambda x, y: x * y)
            R2_mult = getattr(witness, 'R2_mult', lambda x, y: x * y)
            R_mult = getattr(witness, 'R_mult', lambda x, y: (R1_mult(x[0], y[0]), R2_mult(x[1], y[1])))
            
        e1_idemp = (R1_mult(e1, e1) == e1)
        e2_idemp = (R2_mult(e2, e2) == e2)
        R_idemp = (R_mult((e1, e2), (e1, e2)) == (e1, e2))
        
        Q = (R_idemp == (e1_idemp and e2_idemp))
        return [True, True, not Q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R = R1 x R2 is their direct product",
    "H_2: (e1, e2) is an element of R",
    "¬Q: (e1, e2) is idempotent in R iff e1 is idempotent in R1 and e2 is idempotent in R2"
]

N_HYP = 2
NEG_Q_INDEX = 2
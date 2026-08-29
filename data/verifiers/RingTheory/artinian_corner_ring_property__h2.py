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

def conditions(witness) -> list[bool]:
    h1 = False
    q = True
    
    try:
        if isinstance(witness, dict):
            h1 = witness.get("is_right_Artinian", witness.get("R_is_right_Artinian", False))
            q = witness.get("eRe_is_right_Artinian", witness.get("corner_ring_is_right_Artinian", True))
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, e = witness
            h1_val = getattr(R, "is_right_Artinian", False)
            h1 = h1_val() if callable(h1_val) else h1_val
            
            if hasattr(R, "corner_ring"):
                eRe = R.corner_ring(e)
                q_val = getattr(eRe, "is_right_Artinian", True)
                q = q_val() if callable(q_val) else q_val
            elif hasattr(R, "eRe_is_right_Artinian"):
                q_val = R.eRe_is_right_Artinian(e)
                q = q_val() if callable(q_val) else q_val
            else:
                q = True
        else:
            if hasattr(witness, "R") and hasattr(witness, "e"):
                R = witness.R
                e = witness.e
                h1_val = getattr(R, "is_right_Artinian", getattr(witness, "is_right_Artinian", False))
                h1 = h1_val() if callable(h1_val) else h1_val
                
                if hasattr(R, "corner_ring"):
                    eRe = R.corner_ring(e)
                    q_val = getattr(eRe, "is_right_Artinian", True)
                    q = q_val() if callable(q_val) else q_val
                elif hasattr(witness, "eRe"):
                    eRe = witness.eRe
                    q_val = getattr(eRe, "is_right_Artinian", True)
                    q = q_val() if callable(q_val) else q_val
                else:
                    q_val = getattr(witness, "eRe_is_right_Artinian", getattr(witness, "corner_ring_is_right_Artinian", True))
                    q = q_val() if callable(q_val) else q_val
            else:
                h1_val = getattr(witness, "is_right_Artinian", getattr(witness, "R_is_right_Artinian", False))
                h1 = h1_val() if callable(h1_val) else h1_val
                
                q_val = getattr(witness, "eRe_is_right_Artinian", getattr(witness, "corner_ring_is_right_Artinian", True))
                q = q_val() if callable(q_val) else q_val
                
    except Exception:
        pass

    return [bool(h1), not bool(q)]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: The corner ring eRe is not a right Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1
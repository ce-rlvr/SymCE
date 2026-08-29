import sympy
from sympy import MatrixBase, Matrix, S, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: e is an idempotent element of R",
    "¬Q: The corner ring eRe is not a right Artinian ring"
]

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # Parse witness: can be a tuple (R_str, e) or just e
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], str):
            R_str, e = witness
        else:
            e = witness
            R_str = None

        # Convert list of lists to SymPy Matrix
        if isinstance(e, list) and all(isinstance(row, list) for row in e):
            try:
                e = Matrix(e)
            except Exception:
                pass

        # Infer ring if not provided
        if R_str is None:
            if isinstance(e, MatrixBase):
                if all(getattr(val, 'is_integer', False) or isinstance(val, int) for val in e):
                    R_str = f"M_{e.shape[0]}(Z)"
                else:
                    R_str = f"M_{e.shape[0]}(Q)"
            else:
                if getattr(e, 'is_integer', False) or isinstance(e, int):
                    R_str = "Z"
                else:
                    R_str = "Q"

        # Check H_1: e is idempotent
        if isinstance(e, MatrixBase):
            is_idemp = (e * e == e)
        else:
            is_idemp = (e * e == e)
            
        # Check if e is in R
        in_R = False
        if R_str == "Z":
            in_R = (e == 0 or e == 1)
        elif R_str == "Q":
            in_R = (e == 0 or e == 1)
        elif R_str.startswith("M_") and "(Z)" in R_str:
            if isinstance(e, MatrixBase) and e.shape[0] == e.shape[1]:
                in_R = all(getattr(val, 'is_integer', False) or isinstance(val, int) for val in e)
        elif R_str.startswith("M_") and "(Q)" in R_str:
            if isinstance(e, MatrixBase) and e.shape[0] == e.shape[1]:
                in_R = True
        elif R_str in ["Z[x]", "Q[x]"]:
            in_R = (e == 0 or e == 1)
        else:
            in_R = True # Lenient for unknown rings
            
        h1 = bool(is_idemp and in_R)
        
        # Check ¬Q: eRe is NOT right Artinian
        if isinstance(e, MatrixBase):
            is_zero = e.is_zero_matrix
        else:
            is_zero = (e == 0)
            
        if is_zero:
            # The zero ring is Artinian
            neg_q = False
        else:
            # For non-zero idempotents, eRe is Artinian iff the base ring is Artinian
            if R_str in ["Z", "Z[x]", "Q[x]", "Z x Z"] or (R_str.startswith("M_") and "(Z)" in R_str):
                neg_q = True
            elif R_str in ["Q", "R", "C"] or (R_str.startswith("M_") and "(Q)" in R_str):
                neg_q = False
            else:
                # If ring is unknown, we cannot definitively say it's a counterexample
                neg_q = False
                
    except Exception:
        pass
        
    return [h1, neg_q]
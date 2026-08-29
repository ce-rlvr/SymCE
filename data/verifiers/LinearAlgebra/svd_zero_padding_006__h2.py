import sympy
from sympy import Matrix, MatrixBase, eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an m \times n matrix over the complex numbers.
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
        else:
            A, B = witness
        h1_ok = isinstance(A, MatrixBase)
    except Exception:
        h1_ok = False

    # ¬Q: The multiset of strictly positive singular values of B is NOT exactly identical to the multiset of strictly positive singular values of A.
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
        else:
            A, B = witness
            
        if not isinstance(B, MatrixBase) or not isinstance(A, MatrixBase):
            neg_q_ok = False
        else:
            sv_A = A.singular_values()
            sv_B = B.singular_values()
            
            pos_sv_A = []
            for val in sv_A:
                cval = complex(val.evalf())
                if abs(cval) > 1e-9:
                    pos_sv_A.append(float(abs(cval)))
                    
            pos_sv_B = []
            for val in sv_B:
                cval = complex(val.evalf())
                if abs(cval) > 1e-9:
                    pos_sv_B.append(float(abs(cval)))
                    
            pos_sv_A.sort()
            pos_sv_B.sort()
            
            if len(pos_sv_A) != len(pos_sv_B):
                neg_q_ok = True
            else:
                neg_q_ok = False
                for a, b in zip(pos_sv_A, pos_sv_B):
                    if abs(a - b) > 1e-7:
                        neg_q_ok = True
                        break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an m \\times n matrix over the complex numbers",
    "¬Q: The multiset of strictly positive singular values of B is NOT exactly identical to the multiset of strictly positive singular values of A"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, sympy.MatrixBase):
            h1 = False
        elif witness.rows != witness.cols:
            h1 = False
        elif witness.rows == 0:
            h1 = False
        else:
            I = sympy.eye(witness.rows)
            O = sympy.zeros(witness.rows, witness.cols)
            h1 = bool(witness != I and witness != O)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, sympy.MatrixBase) or witness.rows != witness.cols or witness.rows == 0:
            neg_q = False
        else:
            I = sympy.eye(witness.rows)
            norm_P = witness.norm(2)
            norm_I_P = (I - witness).norm(2)
            
            try:
                val_P = float(abs(complex(norm_P.evalf())))
                val_I_P = float(abs(complex(norm_I_P.evalf())))
                neg_q = abs(val_P - val_I_P) > 1e-9
            except TypeError:
                diff = sympy.simplify(norm_P - norm_I_P)
                neg_q = (diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is neither the zero matrix nor the identity matrix",
    "¬Q: The spectral norm of P is not equal to the spectral norm of I - P"
]

N_HYP = 1
NEG_Q_INDEX = 1
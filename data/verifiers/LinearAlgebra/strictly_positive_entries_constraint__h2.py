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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, sympy.matrices.MatrixBase):
            h1 = False
        elif not witness.is_square:
            h1 = False
        else:
            n = witness.rows
            if n < 1:
                h1 = False
            else:
                is_real = all((e.is_real == True) for e in witness)
                if not is_real:
                    h1 = False
                else:
                    diff = witness.T * witness - sympy.eye(n)
                    h1 = all((sympy.simplify(e).is_zero == True) for e in diff)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, sympy.matrices.MatrixBase):
            neg_q = False
        else:
            neg_q = all((e.is_positive == True) for e in witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Q is a real n x n orthogonal matrix",
    "¬Q: All entries of Q are strictly positive"
]

N_HYP = 1
NEG_Q_INDEX = 1
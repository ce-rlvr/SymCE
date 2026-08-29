import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z
import itertools
import functools
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I_1, I_2, ..., I_n are ideals of R",
    "H_2: For all i != j, I_i + I_j = R",
    "¬Q: The product ideal I_1 I_2 ... I_n is not equal to the intersection ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # Setup extraction
    try:
        if isinstance(witness, dict):
            ideals = list(witness.get('ideals', []))
            R = witness.get('R', None)
        elif isinstance(witness, tuple) and len(witness) == 2 and hasattr(witness[1], '__iter__'):
            R = witness[0]
            ideals = list(witness[1])
        elif hasattr(witness, '__iter__') and not isinstance(witness, str):
            ideals = list(witness)
            R = None
        else:
            ideals = []
            R = None
    except Exception:
        ideals = []
        R = None

    # H_1: I_1, I_2, ..., I_n are ideals of R
    try:
        h1 = False
        if ideals and len(ideals) >= 2:
            h1 = True
            for I in ideals:
                # Reject basic types that might accidentally pass duck typing
                if isinstance(I, (int, float, str, bool)):
                    h1 = False
                    break
                # Must support addition and multiplication
                if not (hasattr(I, '__add__') and hasattr(I, '__mul__')):
                    h1 = False
                    break
                # Must support intersection
                if not (hasattr(I, 'intersect') or hasattr(I, 'intersection') or hasattr(I, '__and__')):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # Determine R if not explicitly provided
    try:
        if R is None and h1:
            R = ideals[0] + ideals[1]
    except Exception:
        pass

    # H_2: For all i != j, I_i + I_j = R
    try:
        h2 = False
        if h1 and R is not None:
            h2 = True
            n = len(ideals)
            for i in range(n):
                for j in range(n):
                    if i != j:
                        if (ideals[i] + ideals[j]) != R:
                            h2 = False
                            break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: The product ideal I_1 I_2 ... I_n is not equal to the intersection ideal
    try:
        neg_q = False
        if h1:
            # Compute product
            prod = ideals[0]
            for I in ideals[1:]:
                prod = prod * I
                
            # Compute intersection
            inter = ideals[0]
            for I in ideals[1:]:
                if hasattr(inter, 'intersect'):
                    inter = inter.intersect(I)
                elif hasattr(inter, 'intersection'):
                    inter = inter.intersection(I)
                else:
                    inter = inter & I
                    
            neg_q = bool(prod != inter)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
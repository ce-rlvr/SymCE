import sympy
from sympy.abc import x, y, z
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        if callable(witness):
            res = witness()
            if isinstance(res, (list, tuple)) and len(res) == 3:
                return [bool(res[0]), bool(res[1]), bool(res[2])]
    except Exception:
        pass

    try:
        if isinstance(witness, dict):
            if 'H1' in witness:
                H1 = bool(witness['H1'])
            if 'H2' in witness:
                H2 = bool(witness['H2'])
            if 'neg_Q' in witness:
                neg_Q = bool(witness['neg_Q'])
            elif 'Q' in witness:
                neg_Q = not bool(witness['Q'])
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_equicontinuous'):
            H1 = bool(witness.is_equicontinuous())
        if hasattr(witness, 'is_closure'):
            H2 = bool(witness.is_closure())
        if hasattr(witness, 'closure_is_equicontinuous'):
            neg_Q = not bool(witness.closure_is_equicontinuous())
    except Exception:
        pass

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: F is an equicontinuous family of functions from X to R",
    "H_2: F_bar is the closure of F in the space of all real-valued functions on X under the topology of pointwise convergence",
    "¬Q: The family F_bar is not equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2
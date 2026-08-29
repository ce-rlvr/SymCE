import sympy
from sympy import QQ, ZZ, Rational, Integer
from sympy.abc import x, y, z
import math
import itertools
import functools
import z3

class RingProfile:
    """
    Represents a local ring R, its maximal ideal m, and an element x.
    Since SymPy lacks advanced commutative algebra features (like Krull dimension 
    and localizations of non-Noetherian rings), the witness should be an instance 
    of this class (or a dictionary) providing the mathematically correct properties 
    of a valid counterexample.
    """
    def __init__(self, description: str, x_in_m: bool, x_is_zero_divisor: bool, dim_R: int, dim_R_mod_x: int):
        self.description = str(description)
        self.x_in_m = bool(x_in_m)
        self.x_is_zero_divisor = bool(x_is_zero_divisor)
        self.dim_R = int(dim_R)
        self.dim_R_mod_x = int(dim_R_mod_x)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('x_in_m', False))
        else:
            h1 = bool(witness.x_in_m)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = not bool(witness.get('x_is_zero_divisor', True))
        else:
            h2 = not bool(witness.x_is_zero_divisor)
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            dim_R = int(witness['dim_R'])
            dim_R_mod_x = int(witness['dim_R_mod_x'])
        else:
            dim_R = int(witness.dim_R)
            dim_R_mod_x = int(witness.dim_R_mod_x)
        neg_q = (dim_R_mod_x != dim_R - 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element in m",
    "H_2: x is not a zero divisor in R",
    "¬Q: The Krull dimension of R/(x) is not exactly dim(R) - 1"
]

N_HYP = 2
NEG_Q_INDEX = 2
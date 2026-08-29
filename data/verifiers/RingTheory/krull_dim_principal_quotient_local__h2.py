import sympy
import math

class RingWithElement:
    """
    Mock object to represent a ring R and an element x for the purpose of verifying Krull dimension properties.
    """
    def __init__(self, is_noetherian, is_local, x_is_zero_divisor, dim_R, dim_R_mod_x):
        self.is_noetherian = is_noetherian
        self.is_local = is_local
        self.x_is_zero_divisor = x_is_zero_divisor
        self.dim_R = dim_R
        self.dim_R_mod_x = dim_R_mod_x

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            is_noetherian = bool(witness.get("is_noetherian", False))
            is_local = bool(witness.get("is_local", False))
            x_is_zero_divisor = bool(witness.get("x_is_zero_divisor", True))
            dim_R = float(witness.get("dim_R", 0))
            dim_R_mod_x = float(witness.get("dim_R_mod_x", 0))
        elif isinstance(witness, (list, tuple)) and len(witness) >= 5:
            is_noetherian = bool(witness[0])
            is_local = bool(witness[1])
            x_is_zero_divisor = bool(witness[2])
            dim_R = float(witness[3])
            dim_R_mod_x = float(witness[4])
        else:
            is_noetherian = bool(getattr(witness, "is_noetherian", False))
            is_local = bool(getattr(witness, "is_local", False))
            x_is_zero_divisor = bool(getattr(witness, "x_is_zero_divisor", True))
            dim_R = float(getattr(witness, "dim_R", 0))
            dim_R_mod_x = float(getattr(witness, "dim_R_mod_x", 0))
            
        h1 = is_noetherian and is_local
        h2 = not x_is_zero_divisor
        neg_q = dim_R_mod_x != dim_R - 1.0
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Noetherian local ring",
    "H_2: x is not a zero divisor in R",
    "¬Q: The Krull dimension of R/(x) is not exactly dim(R) - 1"
]

N_HYP = 2
NEG_Q_INDEX = 2
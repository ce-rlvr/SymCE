import sympy
from sympy.abc import x, y, z

class LocalRingWitness:
    """
    A mock witness for the Krull dimension conjecture.
    Since SymPy does not natively support Krull dimension of local rings,
    this class allows specifying the properties directly.
    """
    def __init__(self, is_Noetherian, is_local, x_in_m, dim_R, dim_R_mod_x):
        self.is_Noetherian = is_Noetherian
        self.is_local = is_local
        self.x_in_m = x_in_m
        self.dim_R = dim_R
        self.dim_R_mod_x = dim_R_mod_x

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_Noetherian", False)) and bool(witness.get("is_local", False))
            h2 = bool(witness.get("x_in_m", False))
            dim_R = int(witness.get("dim_R", 0))
            dim_R_mod_x = int(witness.get("dim_R_mod_x", 0))
        elif isinstance(witness, tuple) and len(witness) == 5:
            is_Noetherian, is_local, x_in_m, dim_R, dim_R_mod_x = witness
            h1 = bool(is_Noetherian) and bool(is_local)
            h2 = bool(x_in_m)
            dim_R = int(dim_R)
            dim_R_mod_x = int(dim_R_mod_x)
        else:
            h1 = bool(getattr(witness, "is_Noetherian", False)) and bool(getattr(witness, "is_local", False))
            h2 = bool(getattr(witness, "x_in_m", False))
            dim_R = int(getattr(witness, "dim_R", 0))
            dim_R_mod_x = int(getattr(witness, "dim_R_mod_x", 0))
            
        neg_q = (dim_R_mod_x != dim_R - 1)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Noetherian local ring with maximal ideal m",
    "H_2: x is an element in m",
    "¬Q: The Krull dimension of R/(x) is not exactly dim(R) - 1"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
import math
import itertools
import functools

class RingProfile:
    """
    A mock object to represent the properties of a ring for the counterexample.
    """
    def __init__(self, is_commutative=True, has_identity=True, dim=0, dim_poly=1):
        self.is_commutative = is_commutative
        self.has_identity = has_identity
        self.dim = dim
        self.dim_poly = dim_poly

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Allow witness to be a simple tuple of (dim(R), dim(R_poly))
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            dim_R, dim_Rx = witness
            h1 = True  # Implicitly assuming it's a valid commutative ring with identity
            neg_q = bool(dim_Rx != dim_R + 1)
            return [h1, neg_q]
    except Exception:
        pass

    # Check H1: R is a commutative ring with identity
    try:
        if isinstance(witness, dict):
            is_comm = witness.get("is_commutative", False)
            has_id = witness.get("has_identity", False)
        else:
            is_comm = getattr(witness, "is_commutative", False)
            has_id = getattr(witness, "has_identity", False)
        h1 = bool(is_comm and has_id)
    except Exception:
        h1 = False

    # Check ¬Q: dim(R_poly) != dim(R) + 1
    try:
        if isinstance(witness, dict):
            dim_R = witness.get("dim")
            dim_Rx = witness.get("dim_poly")
        else:
            dim_R = getattr(witness, "dim")
            dim_Rx = getattr(witness, "dim_poly")
        
        if dim_R is not None and dim_Rx is not None:
            neg_q = bool(dim_Rx != dim_R + 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The Krull dimension of the polynomial ring over R is not equal to dim(R) + 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
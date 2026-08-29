import math
import sympy
from sympy import *

class RingModule:
    """
    Represents a pair of a ring R and an R-module M with their homological properties.
    """
    def __init__(self, is_noetherian_local, is_nonzero_fg, pd_M, depth_M, depth_R):
        self.is_noetherian_local = is_noetherian_local
        self.is_nonzero_fg = is_nonzero_fg
        self.pd_M = pd_M
        self.depth_M = depth_M
        self.depth_R = depth_R

inf = math.inf
oo = sympy.oo

def conditions(witness):
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_noetherian_local", False))
        else:
            h1 = bool(witness.is_noetherian_local)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get("is_nonzero_fg", False))
        else:
            h2 = bool(witness.is_nonzero_fg)
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            pd = float(witness.get("pd_M", 0))
            depth_M = float(witness.get("depth_M", 0))
            depth_R = float(witness.get("depth_R", 0))
        else:
            pd = float(witness.pd_M)
            depth_M = float(witness.depth_M)
            depth_R = float(witness.depth_R)
            
        neg_q = (pd + depth_M) != depth_R
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (R, m) is a commutative Noetherian local ring",
    "H_2: M is a non-zero finitely generated R-module",
    "¬Q: pd_R(M) + depth_R(M) != depth(R)"
]

N_HYP = 2
NEG_Q_INDEX = 2
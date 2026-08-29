import sympy
import sympy.abc
import math
import itertools
import functools

class TopologicalSpace:
    def __init__(self, locally_compact, hausdorff, compact, x_star_connected):
        self.locally_compact = locally_compact
        self.hausdorff = hausdorff
        self.compact = compact
        self.x_star_connected = x_star_connected

spaces = {
    "R": TopologicalSpace(True, True, False, True),
    "R2": TopologicalSpace(True, True, False, True),
    "R3": TopologicalSpace(True, True, False, True),
    "N": TopologicalSpace(True, True, False, False),
    "Z": TopologicalSpace(True, True, False, False),
    "Q": TopologicalSpace(False, True, False, False),
    "[0, 1]": TopologicalSpace(True, True, True, True),
    "(0, 1)": TopologicalSpace(True, True, False, True),
    "[0, 1)": TopologicalSpace(True, True, False, True),
    "(0, 1) U (2, 3)": TopologicalSpace(True, True, False, True),
    "[0, 1] U [2, 3]": TopologicalSpace(True, True, True, False),
    "[0, 1] U (2, 3)": TopologicalSpace(True, True, False, False),
    "R U {p}": TopologicalSpace(True, True, False, False),
    "S1": TopologicalSpace(True, True, True, True),
    "discrete_infinite": TopologicalSpace(True, True, False, False),
    "discrete_finite": TopologicalSpace(True, True, True, False),
}

R = spaces["R"]
R2 = spaces["R2"]
R3 = spaces["R3"]
N = spaces["N"]
Z = spaces["Z"]
Q = spaces["Q"]
S1 = spaces["S1"]

def conditions(witness):
    try:
        if isinstance(witness, str) and witness in spaces:
            witness = spaces[witness]
        
        h1 = bool(witness.locally_compact and witness.hausdorff)
        h2 = not bool(witness.compact)
        neg_q = not bool(witness.x_star_connected)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: X is a locally compact Hausdorff space",
    "H_2: X is not compact",
    "¬Q: The one-point compactification X^* is not connected"
]

N_HYP = 2
NEG_Q_INDEX = 2
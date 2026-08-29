import sympy
from sympy import *

class ModuleMock:
    """
    A mock class to represent a module over a ring with specific properties,
    since SymPy does not natively evaluate flatness or torsion-freeness for arbitrary modules.
    """
    def __init__(self, is_module=True, is_flat=False, is_torsion_free=False):
        self._is_module = is_module
        self._is_flat = is_flat
        self._is_torsion_free = is_torsion_free

    def is_module(self):
        return self._is_module

    def is_flat(self):
        return self._is_flat

    def is_torsion_free(self):
        return self._is_torsion_free

# A typical counterexample: the ideal (x, y) in k[x, y] is torsion-free but not flat.
M_counterexample = ModuleMock(is_module=True, is_flat=False, is_torsion_free=True)

def conditions(witness):
    # Allow witness to be a tuple (R, M) or just M
    if isinstance(witness, tuple) and len(witness) == 2:
        M = witness[1]
    else:
        M = witness

    try:
        h1 = bool(M.is_module())
    except Exception:
        h1 = False

    try:
        flat = bool(M.is_flat())
        tf = bool(M.is_torsion_free())
        # The conclusion is "M is flat iff M is torsion-free".
        # It fails if flat is not equal to tf.
        neg_q = (flat != tf)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a module over R",
    "¬Q: Flatness of M is not equivalent to M being torsion-free"
]

N_HYP = 1
NEG_Q_INDEX = 1
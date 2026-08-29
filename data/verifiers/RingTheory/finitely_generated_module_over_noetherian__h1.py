import sympy
from sympy import symbols

# Top-level setup
class CommutativeRing:
    """Representation of a commutative ring for module theory."""
    def __init__(self, name, is_noetherian):
        self.name = name
        self._is_noetherian = is_noetherian

    @property
    def is_noetherian(self):
        return self._is_noetherian

class RModule:
    """Representation of a module over a commutative ring."""
    def __init__(self, ring, generators_count):
        self.ring = ring
        self.generators_count = generators_count

    @property
    def is_R_module(self):
        return isinstance(self.ring, CommutativeRing)

    @property
    def is_finitely_generated(self):
        return self.generators_count < float('inf')

    @property
    def is_noetherian(self):
        if self.generators_count == 0:
            return True
        # A finitely generated free module is Noetherian iff the base ring is Noetherian
        return self.ring.is_noetherian

# Standard rings
Z = CommutativeRing("Z", is_noetherian=True)
Q = CommutativeRing("Q", is_noetherian=True)
PolyRing_inf = CommutativeRing("k[x_1, x_2, ...]", is_noetherian=False)
ContinuousFunctions = CommutativeRing("C(R)", is_noetherian=False)

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(witness.is_R_module)
    except Exception:
        h1 = False

    try:
        h2 = bool(witness.is_finitely_generated)
    except Exception:
        h2 = False

    try:
        neg_q = not bool(witness.is_noetherian)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "H_2: M is finitely generated over R",
    "¬Q: M is not a Noetherian module"
]

N_HYP = 2
NEG_Q_INDEX = 2
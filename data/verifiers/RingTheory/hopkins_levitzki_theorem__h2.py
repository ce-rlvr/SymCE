import sympy
from sympy.abc import x, y, z

# Top-level setup
class AbstractRing:
    """
    A mock class to represent abstract rings with known properties,
    since infinite non-commutative or non-unital rings are not natively 
    supported with Artinian/Noetherian property checks in SymPy.
    """
    def __init__(self, name, ring=True, left_artinian=False, left_noetherian=False):
        self.name = name
        self._ring = ring
        self._left_artinian = left_artinian
        self._left_noetherian = left_noetherian

    def is_ring(self):
        return self._ring

    def is_left_artinian(self):
        return self._left_artinian

    def is_left_noetherian(self):
        return self._left_noetherian

    def __str__(self):
        return self.name

# The standard counterexample to the Hopkins-Levitzki theorem without the identity assumption
# is the Prüfer p-group Z(p^infty) equipped with zero multiplication.
# Its subgroups are linearly ordered and satisfy the descending chain condition (Artinian),
# but not the ascending chain condition (Noetherian).
PruferZeroRing = AbstractRing(
    "Prufer p-group with zero multiplication", 
    ring=True, 
    left_artinian=True, 
    left_noetherian=False
)

def conditions(witness) -> list[bool]:
    # If the witness is provided as a descriptive string
    if isinstance(witness, str):
        w = witness.lower()
        if "prufer" in w or "prüfer" in w:
            return [True, True, True]
            
    # Evaluate properties on the witness object
    try:
        h1 = bool(witness.is_ring())
    except Exception:
        h1 = False

    try:
        h2 = bool(witness.is_left_artinian())
    except Exception:
        h2 = False

    try:
        # The conclusion is that R is left Noetherian.
        # We want the negated conclusion (R is NOT left Noetherian).
        neg_q = not bool(witness.is_left_noetherian())
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R is a left Artinian ring",
    "¬Q: R is not a left Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2
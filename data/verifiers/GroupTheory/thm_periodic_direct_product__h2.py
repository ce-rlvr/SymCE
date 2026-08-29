import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings for the witness expression
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

class InfiniteGroup:
    """A mock class to represent infinite non-periodic groups like Z, R, Q."""
    @property
    def is_periodic(self):
        return False

Z = InfiniteGroup()
R = InfiniteGroup()
Q = InfiniteGroup()

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, H), check if it is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        G, H = witness
    except Exception:
        return [False, False]
    
    def check_periodic(grp):
        # All finite permutation groups are periodic
        if isinstance(grp, PermutationGroup):
            return True
        # Check custom property if available
        if hasattr(grp, 'is_periodic'):
            return grp.is_periodic
        # SymPy FreeGroup is only periodic if it has 0 generators (trivial group)
        if type(grp).__name__ == 'FreeGroup':
            return len(grp.generators) == 0
        return False

    # H_1: G is a periodic group
    try:
        h1_ok = bool(check_periodic(G))
    except Exception:
        h1_ok = False

    # ¬Q: The direct product G x H is NOT a periodic group
    # Note: G x H is periodic if and only if both G and H are periodic.
    try:
        g_periodic = check_periodic(G)
        h_periodic = check_periodic(H)
        g_x_h_periodic = g_periodic and h_periodic
        neg_q_ok = not g_x_h_periodic
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a periodic group",
    "¬Q: The direct product G x H is not a periodic group"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup

# Top-level setup: named object bindings
try:
    from sympy.combinatorics import FreeGroup
    F2 = FreeGroup('x, y')
    F3 = FreeGroup('x, y, z')
except ImportError:
    class NonAmenableGroup:
        pass
    F2 = NonAmenableGroup()
    F3 = NonAmenableGroup()

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_amenable(G):
    """
    Helper function to determine if a group is amenable.
    Finite groups (like PermutationGroup) and Abelian groups are amenable.
    Free groups on >= 2 generators are not amenable.
    """
    if type(G).__name__ == 'NonAmenableGroup':
        return False
    if type(G).__name__ == 'AmenableGroup':
        return True
    if type(G).__name__ == 'FreeGroup':
        try:
            return len(G.generators) <= 1
        except Exception:
            return False
    if isinstance(G, PermutationGroup):
        return True
    if type(G).__name__ in ['SymmetricGroup', 'AlternatingGroup', 'DihedralGroup', 'CyclicGroup']:
        return True
    return False

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, H), checks if it is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
        
    # Hypothesis 1: G is an amenable group
    try:
        h1 = bool(is_amenable(G))
    except Exception:
        h1 = False
        
    # Negated Conclusion: The direct product G x H is NOT an amenable group.
    # A direct product of two groups is amenable if and only if both groups are amenable.
    try:
        g_amenable = is_amenable(G)
        h_amenable = is_amenable(H)
        g_x_h_amenable = g_amenable and h_amenable
        neg_q = not g_x_h_amenable
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is an amenable group",
    "¬Q: The direct product G x H is not an amenable group"
]

N_HYP = 1
NEG_Q_INDEX = 1
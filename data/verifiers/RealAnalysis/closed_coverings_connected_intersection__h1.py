import sympy
from sympy import Interval, Union, Intersection, FiniteSet, EmptySet, S

# Top-level setup: named object bindings that the witness expression may reference.
# For Real Analysis, standard sympy set objects are provided.
R = sympy.S.Reals
N = sympy.S.Naturals
Z = sympy.S.Integers

def is_connected_set(s):
    """Helper to determine if a 1D sympy set is connected."""
    if isinstance(s, sympy.Interval):
        return True
    if isinstance(s, sympy.FiniteSet):
        return len(s) <= 1
    if s == sympy.S.EmptySet:
        return True
    if s == sympy.S.Reals:
        return True
    if isinstance(s, sympy.Union):
        # Sympy automatically simplifies overlapping intervals into a single Interval.
        # If it remains a Union, it consists of disjoint components and is disconnected.
        return False
    if hasattr(s, 'is_connected'):
        return s.is_connected == True
    return False

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness can be a tuple (A, B) where X is implicitly A U B, 
    or a tuple (X, A, B).
    """
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                A, B = witness
                X = A.union(B)
            elif len(witness) == 3:
                X, A, B = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: A and B are closed subsets of X
    try:
        a_sub = (A.is_subset(X) == True)
        b_sub = (B.is_subset(X) == True)
        # A set A is closed in X iff closure(A) \cap X == A
        a_closed = (A.closure.intersect(X) == A)
        b_closed = (B.closure.intersect(X) == B)
        h1 = bool(a_sub and b_sub and a_closed and b_closed)
    except Exception:
        h1 = False

    # H_2: The union A \cup B equals X
    try:
        h2 = bool(A.union(B) == X)
    except Exception:
        h2 = False

    # H_3: The intersection A \cap B is a connected set
    try:
        int_AB = A.intersect(B)
        h3 = bool(is_connected_set(int_AB))
    except Exception:
        h3 = False

    # ¬Q: Both subsets A and B are connected (Conclusion must FAIL)
    # The negation is that AT LEAST ONE of A or B is NOT connected.
    try:
        a_conn = is_connected_set(A)
        b_conn = is_connected_set(B)
        neg_q = not (a_conn and b_conn)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are closed subsets of X",
    "H_2: The union A \\cup B equals X",
    "H_3: The intersection A \\cap B is a connected set",
    "¬Q: At least one of A or B is not connected"
]

N_HYP = 3
NEG_Q_INDEX = 3
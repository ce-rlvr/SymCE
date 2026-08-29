import sympy
from sympy import Interval, FiniteSet, Union, S

# Top-level setup
# (No specific named objects required for this topological/ring theory problem,
# but we rely on sympy's Set classes to represent the topological space and subsets)

def is_compact_hausdorff(X):
    """
    Checks if a sympy Set represents a compact Hausdorff space in the standard topology of Reals.
    By Heine-Borel, a subset of R is compact iff it is closed and bounded.
    """
    if X == S.EmptySet:
        return True
    if isinstance(X, Interval):
        return not X.left_open and not X.right_open and X.start.is_finite and X.end.is_finite
    if isinstance(X, FiniteSet):
        return all(elem.is_real for elem in X)
    if isinstance(X, Union):
        return all(is_compact_hausdorff(arg) for arg in X.args)
    return False

def get_closure(s):
    """
    Computes the closure of a sympy Set in the standard topology of Reals.
    """
    if s == S.EmptySet:
        return s
    if isinstance(s, Interval):
        return Interval(s.start, s.end, False, False)
    if isinstance(s, FiniteSet):
        return s
    if isinstance(s, Union):
        return Union(*[get_closure(arg) for arg in s.args])
    try:
        return s.closure
    except Exception:
        return s

def conditions(witness):
    """
    Given a witness tuple (X, A, B) where X is a topological space and A, B are subsets,
    checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        X, A, B = witness
    except Exception:
        return [False, False, False]
    
    # H_1: X is a compact Hausdorff topological space
    try:
        h1 = bool(is_compact_hausdorff(X))
    except Exception:
        h1 = False
        
    # H_2: R is the ring of continuous real-valued functions on X
    # This implicitly requires A and B to be subsets of X for I_A and I_B to be well-defined ideals in R.
    try:
        h2 = bool(A.is_subset(X) and B.is_subset(X))
    except Exception:
        h2 = False
        
    # ¬Q: The vanishing ideals I_A and I_B are NOT comaximal in R.
    # In C(X), I_A and I_B are comaximal iff the closures of A and B are disjoint.
    # Therefore, they are NOT comaximal iff their closures intersect.
    try:
        cl_A = get_closure(A)
        cl_B = get_closure(B)
        neg_q = bool(cl_A.intersect(cl_B) != S.EmptySet)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact Hausdorff topological space",
    "H_2: R is the ring of continuous real-valued functions on X (A and B are subsets of X)",
    "¬Q: The vanishing ideals I_A and I_B are not comaximal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2
import math
import itertools
import functools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# (No specific named objects required for this RealAnalysis conjecture, 
# but standard symbols are available above)

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: The characteristic function chi_A is uniformly continuous on X",
    "¬Q: The conclusion fails (A is not clopen, or inf d(A, X \\ A) is not strictly greater than zero)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (X, A, d) where:
      - X is an iterable of elements in the metric space
      - A is an iterable of elements in the subset A
      - d is a distance function d(x, y) or a dictionary d[(x, y)]
    """
    try:
        X, A, d = witness
        X_iter = list(X)
        A_iter = list(A)
    except Exception:
        return [False, False, False]

    # H_1: X is a metric space
    h1 = True
    try:
        if len(X_iter) == 0:
            # While empty metric spaces are sometimes allowed, we pass here 
            # and let the metric axioms trivially hold.
            pass
        for u in X_iter:
            for v in X_iter:
                dist = float(d(u, v) if callable(d) else d[(u, v)])
                if dist < 0: 
                    h1 = False
                if (dist == 0.0) != (u == v): 
                    h1 = False
                dist_vu = float(d(v, u) if callable(d) else d[(v, u)])
                if dist != dist_vu: 
                    h1 = False
                for w in X_iter:
                    dist_uw = float(d(u, w) if callable(d) else d[(u, w)])
                    dist_vw = float(d(v, w) if callable(d) else d[(v, w)])
                    if dist_uw > dist + dist_vw + 1e-7: 
                        h1 = False
    except Exception:
        h1 = False

    # H_2: chi_A is uniformly continuous on X
    h2 = True
    try:
        # Check if A is a subset of X
        for a in A_iter:
            if a not in X_iter:
                h2 = False
        
        # For a finite metric space, any function (including chi_A) is uniformly continuous.
        # We don't need to explicitly check epsilon-delta for finite spaces.
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails
    # Conclusion: A is both open and closed in X, and inf d(A, X \ A) > 0.
    neg_q = False
    try:
        distances = []
        for u in A_iter:
            for v in X_iter:
                if v not in A_iter:
                    dist = float(d(u, v) if callable(d) else d[(u, v)])
                    distances.append(dist)
        
        if not distances:
            # If A is empty or A = X, the set of distances between A and X \ A is empty.
            # The infimum of an empty set does not exist in the real numbers.
            # Thus, the statement "the infimum ... is strictly greater than zero" 
            # (which implies it exists as a real number) is False.
            conclusion = False
        else:
            inf_dist = min(distances)
            # In a finite space, every subset is both open and closed.
            # So the conclusion holds iff the infimum of distances is > 0.
            conclusion = (inf_dist > 0)
            
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
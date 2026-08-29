import sympy
from sympy import S, Interval, Union, FiniteSet, Intersection

# Top-level setup
Reals = S.Reals
Naturals = S.Naturals
Integers = S.Integers
Rationals = S.Rationals
EmptySet = S.EmptySet

def conditions(witness):
    # H_1: C is the Cantor ternary set equipped with the standard Euclidean metric
    # The witness is the target space X. We verify it is a valid SymPy Set.
    try:
        h1 = isinstance(witness, sympy.Set)
    except Exception:
        h1 = False

    # neg_Q: There does NOT exist a continuous surjective function f: C -> X
    # By Alexandroff's theorem, a non-empty metric space is a continuous image 
    # of the Cantor set if and only if it is compact.
    # Thus, the conclusion fails (neg_Q is True) iff X is empty or not compact.
    try:
        def is_compact(X):
            if X.is_EmptySet:
                return True
            
            # Check boundedness for subsets of Reals
            try:
                if X.inf.is_infinite or X.sup.is_infinite:
                    return False
            except Exception:
                pass
                
            # Check closedness for standard sets
            if isinstance(X, Interval):
                return not X.left_open and not X.right_open
            if isinstance(X, Union):
                return all(is_compact(arg) for arg in X.args)
            if isinstance(X, FiniteSet):
                return True
                
            # Fallback to boundary check if available
            try:
                if hasattr(X, 'boundary'):
                    return X.boundary.is_subset(X)
            except Exception:
                pass
                
            return False

        if not isinstance(witness, sympy.Set):
            neg_q = False
        elif witness.is_EmptySet:
            neg_q = True
        else:
            neg_q = not is_compact(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: C is the Cantor ternary set equipped with the standard Euclidean metric",
    "¬Q: There does not exist a continuous surjective function f: C -> X"
]

N_HYP = 1
NEG_Q_INDEX = 1
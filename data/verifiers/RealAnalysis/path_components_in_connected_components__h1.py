import sympy
from sympy import Interval, FiniteSet, Union, Intersection, EmptySet, Set
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_connected_components(X):
    """
    Helper function to compute connected/path components for basic SymPy sets
    and Python sets. For subsets of R, path components and connected components coincide.
    """
    if isinstance(X, set):
        return [{x} for x in X]
    if isinstance(X, Set):
        if X.is_EmptySet:
            return []
        if isinstance(X, Interval):
            return [X]
        if isinstance(X, FiniteSet):
            return [FiniteSet(x) for x in X.args]
        if isinstance(X, Union):
            comps = []
            for arg in X.args:
                if isinstance(arg, FiniteSet):
                    comps.extend([FiniteSet(x) for x in arg.args])
                else:
                    comps.append(arg)
            return comps
        return [X]
    return []

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (X, P, C) representing the space X, 
    the path component P, and the connected component C.
    """
    try:
        X, P, C = witness
    except Exception:
        return [False, False, False, False]

    def to_sympy_set(obj):
        if isinstance(obj, (set, list, tuple)):
            return FiniteSet(*obj)
        return obj

    # Normalize types to avoid mixing SymPy sets and Python sets
    try:
        if isinstance(X, Set) or isinstance(P, Set) or isinstance(C, Set):
            X = to_sympy_set(X)
            P = to_sympy_set(P)
            C = to_sympy_set(C)
        else:
            if isinstance(X, (list, tuple)): X = set(X)
            if isinstance(P, (list, tuple)): P = set(P)
            if isinstance(C, (list, tuple)): C = set(C)
    except Exception:
        pass

    # H_1: P is a path component of X
    try:
        if hasattr(X, 'path_components'):
            h1 = P in X.path_components()
        else:
            h1 = P in get_connected_components(X)
    except Exception:
        h1 = False

    # H_2: C is a connected component of X
    try:
        if hasattr(X, 'connected_components'):
            h2 = C in X.connected_components()
        else:
            h2 = C in get_connected_components(X)
    except Exception:
        h2 = False

    # H_3: The intersection of P and C is non-empty
    try:
        if isinstance(P, set) and isinstance(C, set):
            h3 = len(P.intersection(C)) > 0
        elif hasattr(P, 'intersection'):
            inter = P.intersection(C)
            if isinstance(inter, (set, list, tuple)):
                h3 = len(inter) > 0
            else:
                h3 = not inter.is_EmptySet
        else:
            inter = Intersection(P, C)
            h3 = not inter.is_EmptySet
    except Exception:
        h3 = False

    # ¬Q: P is not a subset of C
    try:
        if isinstance(P, set) and isinstance(C, set):
            neg_q = not P.issubset(C)
        elif hasattr(P, 'issubset'):
            neg_q = not P.issubset(C)
        elif hasattr(P, 'is_subset'):
            neg_q = not P.is_subset(C)
        else:
            # Fallback for general iterables
            neg_q = not all(p in C for p in P)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P is a path component of X",
    "H_2: C is a connected component of X",
    "H_3: The intersection of P and C is non-empty",
    "¬Q: P is not a subset of C"
]

N_HYP = 3
NEG_Q_INDEX = 3
import sympy
from sympy import S, Interval, FiniteSet, Union, Intersection, ProductSet, Set

def get_set(witness, n):
    """Helper to extract the n-th set from the witness."""
    if callable(witness):
        return witness(n)
    elif isinstance(witness, dict):
        return witness[n]
    else:
        # Assume 0-indexed list/tuple, but n is 1-based
        return witness[n-1]

def is_compact(s):
    """Check if a Sympy Set is compact (closed and bounded in R^n)."""
    if s == S.EmptySet:
        return True
    if isinstance(s, FiniteSet):
        return True
    if isinstance(s, Interval):
        return (not s.left_open) and (not s.right_open) and (s.inf != S.NegativeInfinity) and (s.sup != S.Infinity)
    if isinstance(s, Union):
        return all(is_compact(arg) for arg in s.args)
    if isinstance(s, Intersection):
        # Intersection of closed sets is closed; if at least one is bounded, it is bounded.
        return any(is_compact(arg) for arg in s.args)
    if isinstance(s, ProductSet):
        return all(is_compact(arg) for arg in s.sets)
    return False

def is_connected(s):
    """Check if a Sympy Set is connected."""
    if s == S.EmptySet:
        return True
    if isinstance(s, FiniteSet):
        return len(s) <= 1
    if isinstance(s, Interval):
        return True
    if isinstance(s, Union):
        # Sympy automatically simplifies unions of overlapping intervals.
        # If it remains a Union, it is composed of disjoint sets.
        return len(s.args) <= 1
    if isinstance(s, Intersection):
        # Intersection of intervals/convex sets is convex, hence connected.
        return True
    if isinstance(s, ProductSet):
        return all(is_connected(arg) for arg in s.sets)
    return False

def conditions(witness) -> list[bool]:
    N_MAX = 5
    
    # H_1: X is a Hausdorff topological space
    # We assume the sets are subsets of R or R^n, which are Hausdorff.
    h1 = True
    
    # H_2: C_n is a sequence of subsets of X
    h2 = True
    try:
        for n in range(1, N_MAX + 1):
            s = get_set(witness, n)
            if not isinstance(s, Set):
                h2 = False
                break
    except Exception:
        h2 = False
        
    # H_3: C_n is compact for all n >= 1
    h3 = True
    try:
        for n in range(1, N_MAX + 1):
            s = get_set(witness, n)
            if not is_compact(s):
                h3 = False
                break
    except Exception:
        h3 = False
        
    # H_4: C_n is connected for all n >= 1
    h4 = True
    try:
        for n in range(1, N_MAX + 1):
            s = get_set(witness, n)
            if not is_connected(s):
                h4 = False
                break
    except Exception:
        h4 = False
        
    # H_5: C_{n+1} \subseteq C_n for all n >= 1
    h5 = True
    try:
        for n in range(1, N_MAX):
            s1 = get_set(witness, n)
            s2 = get_set(witness, n+1)
            if not s2.is_subset(s1):
                h5 = False
                break
    except Exception:
        h5 = False
        
    # neg_Q: The intersection is empty or disconnected
    neg_q = False
    try:
        inter = get_set(witness, 1)
        for n in range(2, N_MAX + 1):
            inter = Intersection(inter, get_set(witness, n))
            
        is_non_empty = (inter != S.EmptySet)
        is_conn = is_connected(inter)
        
        # The conclusion is that the intersection is non-empty AND connected.
        # The negation is that it is empty OR disconnected.
        if not (is_non_empty and is_conn):
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: X is a Hausdorff topological space",
    "H_2: C_n is a sequence of subsets of X",
    "H_3: C_n is compact for all n >= 1",
    "H_4: C_n is connected for all n >= 1",
    "H_5: C_{n+1} is a subset of C_n for all n >= 1",
    "¬Q: The intersection is empty or disconnected"
]

N_HYP = 5
NEG_Q_INDEX = 5
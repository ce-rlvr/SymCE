import itertools

# Top-level setup
# A witness is expected to be a tuple (X, T) where X is an iterable of points 
# and T is an iterable of subsets of X (representing the open sets of the topology).

def conditions(witness) -> list[bool]:
    try:
        X, T = witness
        X = frozenset(X)
        T_frozen = set(frozenset(U) for U in T)
    except Exception:
        return [False, False]
    
    # H_1: X is a topological space
    try:
        h1 = True
        # 1. The empty set and X must be in the topology
        if frozenset() not in T_frozen or X not in T_frozen:
            h1 = False
        
        # 2. The topology must be closed under finite unions and intersections
        if h1:
            for U in T_frozen:
                for V in T_frozen:
                    if U.union(V) not in T_frozen:
                        h1 = False
                        break
                    if U.intersection(V) not in T_frozen:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # ¬Q: X is not connected
    # A space is not connected if it can be partitioned into two non-empty disjoint open sets.
    try:
        neg_q = False
        for U in T_frozen:
            if not U:
                continue
            for V in T_frozen:
                if not V:
                    continue
                if not U.intersection(V) and U.union(V) == X:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "¬Q: X is not connected"
]

N_HYP = 1
NEG_Q_INDEX = 1
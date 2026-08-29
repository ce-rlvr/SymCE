import itertools

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture:
    "Let X be a topological space. Then X is totally disconnected."
    
    Expected witness format: A tuple (X, T) where X is an iterable of elements
    and T is an iterable of subsets of X (the open sets).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
            
        X_raw, T_raw = witness
        X = frozenset(X_raw)
        T = frozenset(frozenset(s) for s in T_raw)
    except Exception:
        return [False, False]
        
    # H_1: X is a topological space
    h1_ok = False
    try:
        # Restrict sizes to ensure fast evaluation
        if len(X) <= 20 and len(T) <= 256:
            has_empty = frozenset() in T
            has_X = X in T
            subsets_ok = all(s.issubset(X) for s in T)
            intersections_ok = all(A.intersection(B) in T for A in T for B in T)
            unions_ok = all(A.union(B) in T for A in T for B in T)
            
            h1_ok = has_empty and has_X and subsets_ok and intersections_ok and unions_ok
    except Exception:
        h1_ok = False

    # neg_Q: X is not totally disconnected
    # A space is totally disconnected if its only connected components are singletons (or empty).
    # Thus, it is NOT totally disconnected if there exists a connected subset of size > 1.
    neg_q_ok = False
    try:
        if len(X) <= 20 and len(T) <= 256:
            def is_connected(C):
                # C is disconnected if there exist open sets U, V in T such that
                # U ∩ C and V ∩ C are disjoint, non-empty, and their union is C.
                for U in T:
                    for V in T:
                        U_C = U.intersection(C)
                        V_C = V.intersection(C)
                        if U_C and V_C and U_C.isdisjoint(V_C) and U_C.union(V_C) == C:
                            return False
                return True
            
            # Check all subsets of size > 1
            for r in range(2, len(X) + 1):
                for subset in itertools.combinations(X, r):
                    C = frozenset(subset)
                    if is_connected(C):
                        neg_q_ok = True
                        break
                if neg_q_ok:
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "¬Q: X is not totally disconnected"
]

N_HYP = 1
NEG_Q_INDEX = 1
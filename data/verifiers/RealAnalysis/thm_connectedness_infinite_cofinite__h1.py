import itertools

def conditions(witness):
    try:
        is_tau_collection = False
        if isinstance(witness, tuple) and len(witness) == 2:
            try:
                # Check if witness[1] looks like a topology (iterable of iterables)
                _ = set(frozenset(U) for U in witness[1])
                is_tau_collection = True
            except Exception:
                pass

        if is_tau_collection:
            X, tau = witness
        elif isinstance(witness, int):
            if witness < 0 or witness > 15:
                return [False, False]
            X = list(range(witness))
            X_set = frozenset(X)
            def powerset(iterable):
                s = list(iterable)
                return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))
            tau = list(powerset(X_set))
        else:
            X = witness
            X_set = frozenset(X)
            if len(X_set) > 15:
                return [False, False]
            def powerset(iterable):
                s = list(iterable)
                return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))
            tau = list(powerset(X_set))
            
        X_set = frozenset(X)
        tau_sets = set(frozenset(U) for U in tau)
    except Exception:
        return [False, False]
        
    # H_1: tau is the cofinite topology on X
    try:
        if len(X_set) > 15:
            h1_ok = False
        else:
            def powerset(iterable):
                s = list(iterable)
                return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))
            
            expected_tau = set(frozenset(U) for U in powerset(X_set))
            h1_ok = (tau_sets == expected_tau)
    except Exception:
        h1_ok = False

    # neg_Q: (X, tau) is disconnected
    try:
        neg_q_ok = False
        for U in tau_sets:
            if not U:
                continue
            for V in tau_sets:
                if not V:
                    continue
                if U.isdisjoint(V) and U.union(V) == X_set:
                    neg_q_ok = True
                    break
            if neg_q_ok:
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: tau is the cofinite topology on X",
    "¬Q: The topological space (X, tau) is not connected"
]

N_HYP = 1
NEG_Q_INDEX = 1
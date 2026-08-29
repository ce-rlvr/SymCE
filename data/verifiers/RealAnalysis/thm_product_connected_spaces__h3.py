import itertools

# Top-level setup
# (No specific named objects are required for general topological spaces)

def is_topology(X, T):
    try:
        X_set = frozenset(X)
        T_sets = set(frozenset(s) for s in T)
        if frozenset() not in T_sets or X_set not in T_sets:
            return False
        for A in T_sets:
            if not A.issubset(X_set):
                return False
            for B in T_sets:
                if A.intersection(B) not in T_sets:
                    return False
                if A.union(B) not in T_sets:
                    return False
        return True
    except Exception:
        return False

def is_connected(X, T):
    try:
        X_set = frozenset(X)
        T_sets = set(frozenset(s) for s in T)
        # A space is connected if it cannot be partitioned into two non-empty open sets.
        # i.e., there is no proper non-empty subset that is both open and closed.
        for U in T_sets:
            if U != frozenset() and U != X_set:
                V = X_set - U
                if V in T_sets:
                    return False
        return True
    except Exception:
        return False

def product_space(X_space, Y_space):
    X, T_X = X_space
    Y, T_Y = Y_space
    
    X_set = frozenset(X)
    Y_set = frozenset(Y)
    
    prod_X = frozenset((x, y) for x in X_set for y in Y_set)
    
    T_X_sets = set(frozenset(s) for s in T_X)
    T_Y_sets = set(frozenset(s) for s in T_Y)
    
    basis = set()
    for U in T_X_sets:
        for V in T_Y_sets:
            basis.add(frozenset((x, y) for x in U for y in V))
            
    T_prod = set(basis)
    added = True
    while added:
        added = False
        new_sets = set()
        for A in T_prod:
            for B in basis:
                C = A.union(B)
                if C not in T_prod:
                    new_sets.add(C)
        if new_sets:
            T_prod.update(new_sets)
            added = True
            
    return prod_X, T_prod

def get_spaces(witness):
    if isinstance(witness, dict):
        return witness['X'], witness['Y']
    else:
        return witness[0], witness[1]

def conditions(witness):
    try:
        X_space, Y_space = get_spaces(witness)
    except Exception:
        return [False, False, False]

    try:
        X, T_X = X_space
        h1 = is_topology(X, T_X) and is_connected(X, T_X)
    except Exception:
        h1 = False

    try:
        Y, T_Y = Y_space
        h2 = is_topology(Y, T_Y) and is_connected(Y, T_Y)
    except Exception:
        h2 = False

    try:
        prod_X, T_prod = product_space(X_space, Y_space)
        neg_q = not is_connected(prod_X, T_prod)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a connected topological space",
    "H_2: Y is a connected topological space",
    "¬Q: The product space X × Y is not connected"
]

N_HYP = 2
NEG_Q_INDEX = 2
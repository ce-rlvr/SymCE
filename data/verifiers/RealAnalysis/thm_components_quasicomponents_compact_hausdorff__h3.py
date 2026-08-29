import sympy
import itertools
import functools
import math

# Top-level setup
N = sympy.S.Naturals
Z = sympy.S.Integers
R = sympy.S.Reals
Q = sympy.S.Rationals

def is_topological_space(X, T):
    try:
        X_set = frozenset(X)
        T_sets = [frozenset(t) for t in T]
    except Exception:
        return False
    if frozenset() not in T_sets or X_set not in T_sets:
        return False
    for t1 in T_sets:
        for t2 in T_sets:
            if t1.intersection(t2) not in T_sets:
                return False
    for t1 in T_sets:
        for t2 in T_sets:
            if t1.union(t2) not in T_sets:
                return False
    return True

def is_compact(X, T):
    # Any finite topological space is compact
    return True

def get_clopen_sets(X, T):
    T_sets = [frozenset(t) for t in T]
    X_set = frozenset(X)
    closed_sets = [X_set - t for t in T_sets]
    clopen = []
    for t in T_sets:
        if t in closed_sets:
            clopen.append(t)
    return clopen

def quasi_component(X, T, x):
    clopen = get_clopen_sets(X, T)
    q_x = frozenset(X)
    for c in clopen:
        if x in c:
            q_x = q_x.intersection(c)
    return q_x

def connected_component(X, T, x):
    T_sets = [frozenset(t) for t in T]
    
    def is_connected(S):
        S_set = frozenset(S)
        if not S_set:
            return True
        sub_topology = {S_set.intersection(t) for t in T_sets}
        for A in sub_topology:
            if not A: continue
            if A == S_set: continue
            B = S_set - A
            if B in sub_topology:
                return False
        return True

    X_list = list(X)
    if len(X_list) <= 12:
        for r in range(len(X_list), 0, -1):
            for subset in itertools.combinations(X_list, r):
                if x in subset and is_connected(subset):
                    return frozenset(subset)
    return quasi_component(X, T, x)

def conditions(witness):
    try:
        if callable(witness):
            witness = witness()
    except Exception:
        pass

    h1, h2, neg_q = False, False, False

    # 1. Try tuple (X, T) or dict with X, T (Finite space representation)
    try:
        X_val, T_val = None, None
        if isinstance(witness, tuple) and len(witness) == 2:
            X_val, T_val = witness
        elif isinstance(witness, dict) and 'X' in witness and 'T' in witness:
            X_val, T_val = witness['X'], witness['T']
            
        if X_val is not None and T_val is not None:
            if isinstance(X_val, (list, set, frozenset, tuple)):
                h1 = is_topological_space(X_val, T_val)
                h2 = is_compact(X_val, T_val)
                for x in X_val:
                    c_x = connected_component(X_val, T_val, x)
                    q_x = quasi_component(X_val, T_val, x)
                    if c_x != q_x:
                        neg_q = True
                        break
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try object methods (Infinite space mock object representation)
    try:
        has_topo = False
        if hasattr(witness, 'is_topological_space'):
            h1 = bool(witness.is_topological_space())
            has_topo = True
        elif hasattr(witness, 'check_topological_space'):
            h1 = bool(witness.check_topological_space())
            has_topo = True

        if hasattr(witness, 'is_compact'):
            h2 = bool(witness.is_compact())
        elif hasattr(witness, 'check_compact'):
            h2 = bool(witness.check_compact())

        if has_topo and hasattr(witness, 'connected_component') and hasattr(witness, 'quasi_component'):
            points = []
            if hasattr(witness, 'points'):
                points = witness.points
            elif hasattr(witness, 'X'):
                points = witness.X
            elif hasattr(witness, 'get_points'):
                points = witness.get_points()
            
            for x in points:
                if witness.connected_component(x) != witness.quasi_component(x):
                    neg_q = True
                    break
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try dictionary with explicit properties
    try:
        if isinstance(witness, dict) and ('components' in witness or 'quasi_components' in witness):
            h1 = bool(witness.get('is_topological_space', True))
            h2 = bool(witness.get('is_compact', True))
            X_val = witness.get('X', witness.get('points', []))
            comps = witness.get('components', {})
            qcomps = witness.get('quasi_components', {})
            for x in X_val:
                if comps.get(x) != qcomps.get(x):
                    neg_q = True
                    break
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: X is a compact space",
    "¬Q: There exists a point x in X such that the connected component of x is not equal to the quasi-component of x"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import eye, zeros, Set
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: K is a compact subset of X",
    "¬Q: K is not closed and bounded in X"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # 1. Duck typing for custom objects
    try:
        if hasattr(witness, 'is_compact') and hasattr(witness, 'is_closed') and hasattr(witness, 'is_bounded'):
            h1 = witness.is_compact() if callable(witness.is_compact) else witness.is_compact
            is_closed = witness.is_closed() if callable(witness.is_closed) else witness.is_closed
            is_bounded = witness.is_bounded() if callable(witness.is_bounded) else witness.is_bounded
            
            q = is_closed and is_bounded
            return [bool(h1), not bool(q)]
    except Exception:
        pass

    # 2. Dictionary with boolean flags or explicit X, T, K
    try:
        if isinstance(witness, dict):
            if 'is_compact' in witness and 'is_closed' in witness and 'is_bounded' in witness:
                h1 = witness['is_compact']
                is_closed = witness['is_closed']
                is_bounded = witness['is_bounded']
                q = is_closed and is_bounded
                return [bool(h1), not bool(q)]
            
            if 'X' in witness and 'K' in witness:
                if 'T' in witness:
                    witness = (witness['X'], witness['T'], witness['K'])
                elif 'd' in witness:
                    witness = (witness['X'], witness['d'], witness['K'])
    except Exception:
        pass

    # 3. Tuple (X, T, K) or (X, d, K)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            X, second, K = witness
            X_fs = frozenset(X)
            K_fs = frozenset(K)
            
            if not K_fs.issubset(X_fs):
                return [False, False]
                
            # Check if second is a topology
            is_topology = False
            if isinstance(second, (list, set, tuple)):
                try:
                    T_fs = [frozenset(U) for U in second]
                    is_topology = True
                except Exception:
                    pass
            
            if is_topology:
                if frozenset() not in T_fs or X_fs not in T_fs:
                    is_topology = False
                else:
                    for U in T_fs:
                        for V in T_fs:
                            if U.union(V) not in T_fs:
                                is_topology = False
                                break
                            if U.intersection(V) not in T_fs:
                                is_topology = False
                                break
                        if not is_topology:
                            break
                            
            if is_topology:
                h1 = True  # In a finite topological space, all subsets are compact
                is_closed = X_fs.difference(K_fs) in T_fs
                is_bounded = True  # Boundedness is trivially true or undefined in general topology
                q = is_closed and is_bounded
                return [h1, not q]
                
            # Check if second is a metric or pseudo-metric
            is_metric = False
            if isinstance(second, dict) or callable(second):
                d = second
                def dist(x, y):
                    if callable(d): return d(x, y)
                    return d.get((x, y), d.get((y, x), 0))
                    
                try:
                    valid_metric = True
                    for x in X:
                        if bool(dist(x, x) != 0): valid_metric = False
                        for y in X:
                            if bool(dist(x, y) != dist(y, x)): valid_metric = False
                            for z in X:
                                if bool(dist(x, z) > dist(x, y) + dist(y, z)): valid_metric = False
                    is_metric = valid_metric
                except Exception:
                    is_metric = False
                    
            if is_metric:
                h1 = True  # Finite space is always compact
                def is_open(U):
                    for x in U:
                        for y in X_fs.difference(U):
                            if bool(dist(x, y) == 0):
                                return False
                    return True
                    
                is_closed = is_open(X_fs.difference(K_fs))
                is_bounded = True  # Finite space is always bounded
                q = is_closed and is_bounded
                return [h1, not q]
    except Exception:
        pass

    # 4. Sympy Set
    try:
        if isinstance(witness, Set):
            h1 = witness.is_compact
            is_closed = witness.is_closed
            is_bounded = witness.is_bounded
            if h1 is not None and is_closed is not None and is_bounded is not None:
                q = is_closed and is_bounded
                return [bool(h1), not bool(q)]
    except Exception:
        pass

    return [False, False]
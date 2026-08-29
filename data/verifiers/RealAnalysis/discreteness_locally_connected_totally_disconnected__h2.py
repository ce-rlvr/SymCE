import sympy
import itertools

# Top-level setup
Q = sympy.S.Rationals
R = sympy.S.Reals
Z = sympy.S.Integers
N = sympy.S.Naturals

def evaluate_string(w):
    w = w.lower().strip()
    if w in ['q', 'rationals', 'rational numbers']:
        return True, True, False
    if w in ['r', 'reals', 'real numbers']:
        return True, False, False
    if w in ['z', 'integers', 'n', 'naturals']:
        return True, True, True
    if w in ['cantor', 'cantor set', 'cantor space']:
        return True, True, False
    if w in ['baire', 'baire space']:
        return True, True, False
    if w in ['sorgenfrey', 'sorgenfrey line']:
        return True, True, False
    raise ValueError("Unknown string witness")

def evaluate_sympy_set(w):
    if w == sympy.S.Rationals:
        return True, True, False
    if w in (sympy.S.Integers, sympy.S.Naturals, sympy.S.Naturals0):
        return True, True, True
    if w == sympy.S.Reals:
        return True, False, False
    if w.is_FiniteSet:
        return True, True, True
    if isinstance(w, sympy.Complement) and w.args[0] == sympy.S.Reals and w.args[1] == sympy.S.Rationals:
        return True, True, False
    if isinstance(w, sympy.Interval):
        if w.left == w.right:
            return True, True, True
        else:
            return True, False, False
    raise ValueError("Unknown SymPy set witness")

def check_finite_space(X, T):
    X_set = frozenset(X)
    T_sets = [frozenset(s) for s in T]
    
    if frozenset() not in T_sets or X_set not in T_sets:
        return False, False, False
    
    for s1 in T_sets:
        for s2 in T_sets:
            if s1.intersection(s2) not in T_sets:
                return False, False, False
            if s1.union(s2) not in T_sets:
                return False, False, False
                
    def is_connected(S):
        S = frozenset(S)
        if len(S) <= 1:
            return True
        rel_opens = {S.intersection(u) for u in T_sets}
        for A in rel_opens:
            if len(A) > 0 and len(A) < len(S):
                B = S - A
                if B in rel_opens:
                    return False
        return True

    totally_disconnected = True
    for r in range(2, len(X_set) + 1):
        for subset in itertools.combinations(X_set, r):
            if is_connected(subset):
                totally_disconnected = False
                break
        if not totally_disconnected:
            break

    discrete = all(frozenset([x]) in T_sets for x in X_set)
    
    return True, totally_disconnected, discrete

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'is_topological_space'):
            h1 = witness.is_topological_space()
            h2 = witness.is_totally_disconnected()
            q = witness.is_discrete()
            return [bool(h1), bool(h2), not bool(q)]
    except Exception:
        pass

    try:
        if isinstance(witness, str):
            h1, h2, q = evaluate_string(witness)
            return [h1, h2, not q]
    except Exception:
        pass

    try:
        if isinstance(witness, sympy.Set):
            h1, h2, q = evaluate_sympy_set(witness)
            return [h1, h2, not q]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            X, T = witness
            if isinstance(X, (list, set, frozenset, tuple)) and isinstance(T, (list, set, frozenset, tuple)):
                h1, h2, q = check_finite_space(X, T)
                return [h1, h2, not q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: X is totally disconnected",
    "¬Q: X is not a discrete topological space"
]

N_HYP = 2
NEG_Q_INDEX = 2
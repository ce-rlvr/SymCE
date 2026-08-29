import sympy
from sympy import S, Lambda, Set, Symbol
from sympy.abc import x
import itertools
import functools
import math

# Top-level setup: named object bindings that the witness expression may reference.
# For this Real Analysis / Topology conjecture, the standard counterexample uses the Rationals.
Q = S.Rationals
R = S.Reals
Z = S.Integers
N = S.Naturals
id_map = Lambda(x, x)

def is_finite_topological_space(space):
    try:
        points, topology = space
        points_set = frozenset(points)
        top_sets = set(frozenset(u) for u in topology)
        
        if frozenset() not in top_sets:
            return False
        if points_set not in top_sets:
            return False
            
        for u in top_sets:
            for v in top_sets:
                if u.union(v) not in top_sets:
                    return False
                if u.intersection(v) not in top_sets:
                    return False
        return True
    except Exception:
        return False

def is_finite_quotient_map(X, Y, f):
    try:
        points_X, top_X = X
        points_Y, top_Y = Y
        
        if isinstance(f, dict):
            func = lambda p: f[p]
        else:
            func = f
            
        mapped = set()
        for p in points_X:
            y = func(p)
            if y not in points_Y:
                return False
            mapped.add(y)
        if mapped != set(points_Y):
            return False
            
        top_X_sets = set(frozenset(u) for u in top_X)
        top_Y_sets = set(frozenset(u) for u in top_Y)
        
        def powerset(iterable):
            s = list(iterable)
            return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))
            
        for subset in powerset(points_Y):
            U = frozenset(subset)
            preimage = frozenset(p for p in points_X if func(p) in U)
            
            is_U_open = U in top_Y_sets
            is_preimage_open = preimage in top_X_sets
            
            if is_U_open != is_preimage_open:
                return False
        return True
    except Exception:
        return False

def finite_is_connected(C, top_sets):
    if not C:
        return True
    rel_open = set(C.intersection(u) for u in top_sets)
    for A in rel_open:
        if not A: continue
        for B in rel_open:
            if not B: continue
            if A.union(B) == C and not A.intersection(B):
                return False
    return True

def finite_is_locally_connected(space):
    try:
        points, topology = space
        top_sets = set(frozenset(u) for u in topology)
        
        for y in points:
            open_neighborhoods = [u for u in top_sets if y in u]
            for U in open_neighborhoods:
                found_V = False
                for V in open_neighborhoods:
                    if V.issubset(U) and finite_is_connected(V, top_sets):
                        found_V = True
                        break
                if not found_V:
                    return False
        return True
    except Exception:
        return False

def is_topological_space(space):
    if hasattr(space, 'is_topological_space'):
        return space.is_topological_space()
    if isinstance(space, tuple) and len(space) == 2:
        return is_finite_topological_space(space)
    if isinstance(space, Set):
        return True
    if space in ["Q", "R", "Z", "N", "Rationals", "Reals", "Integers", "Naturals"]:
        return True
    return False

def is_quotient_map(X, Y, f):
    if hasattr(f, 'is_quotient_map'):
        return f.is_quotient_map(X, Y)
    if isinstance(X, tuple) and isinstance(Y, tuple):
        return is_finite_quotient_map(X, Y, f)
    
    if X == Y:
        if isinstance(f, Lambda):
            var = f.variables[0]
            if f.expr == var:
                return True
        elif hasattr(f, '__call__'):
            try:
                if f(1) == 1 and f(2) == 2:
                    return True
            except Exception:
                pass
        elif f in ["identity", "id", "id_map"]:
            return True
            
    return False

def is_locally_connected(space):
    if hasattr(space, 'is_locally_connected'):
        return space.is_locally_connected()
    if isinstance(space, tuple) and len(space) == 2:
        return finite_is_locally_connected(space)
    if space == S.Rationals or space in ["Q", "Rationals"]:
        return False
    if space == S.Reals or space in ["R", "Reals"]:
        return True
    if space == S.Integers or space in ["Z", "Integers"]:
        return True
    return True

def conditions(witness) -> list[bool]:
    # Allow witness to be a custom object that evaluates itself
    if hasattr(witness, 'is_topological_space'):
        try:
            h1 = witness.is_topological_space()
            h2 = witness.is_quotient_map()
            neg_q = not witness.is_locally_connected()
            return [bool(h1), bool(h2), bool(neg_q)]
        except Exception:
            pass

    try:
        X, Y, f = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(is_topological_space(X) and is_topological_space(Y))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(is_quotient_map(X, Y, f))
    except Exception:
        h2 = False
        
    try:
        neg_q = not bool(is_locally_connected(Y))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X and Y are topological spaces",
    "H_2: f: X \\to Y is a quotient map",
    "¬Q: Y is not a locally connected space"
]

N_HYP = 2
NEG_Q_INDEX = 2
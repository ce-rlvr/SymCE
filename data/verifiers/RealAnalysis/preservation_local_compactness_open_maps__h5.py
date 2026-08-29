import sympy
from sympy import S, Interval, Union, Intersection, FiniteSet, Lambda, Symbol, Complement

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
R = S.Reals
Q = S.Rationals
Z = S.Integers
N = S.Naturals

def is_metric_space(space):
    if hasattr(space, 'is_metric_space'):
        return space.is_metric_space()
    try:
        return space.is_subset(S.Reals) == True
    except Exception:
        return False

def is_locally_compact(space):
    if hasattr(space, 'is_locally_compact'):
        return space.is_locally_compact()
    try:
        if space in (S.Reals, S.Integers, S.Naturals, S.EmptySet):
            return True
        if space == S.Rationals:
            return False
        if isinstance(space, Interval):
            return True
        if isinstance(space, FiniteSet):
            return True
        if isinstance(space, Union):
            if S.Rationals in space.args:
                return False
            return all(is_locally_compact(arg) for arg in space.args)
        if isinstance(space, Intersection):
            if S.Rationals in space.args:
                return False
        if isinstance(space, Complement):
            if space.args[1] == S.Rationals:
                return False
        return False
    except Exception:
        return False

def is_open_in_R(space):
    if hasattr(space, 'is_open'):
        return space.is_open()
    try:
        if space in (S.Reals, S.EmptySet):
            return True
        if isinstance(space, Interval):
            return space.left_open and space.right_open
        if isinstance(space, Union):
            return all(is_open_in_R(arg) for arg in space.args)
        return False
    except Exception:
        return False

def is_valid_map(f, X, Y):
    if hasattr(f, 'is_valid_map'):
        return f.is_valid_map(X, Y)
    if isinstance(f, dict) and f.get('type') == 'inclusion':
        try:
            return X.is_subset(Y) == True
        except Exception:
            return False
    try:
        if isinstance(f, Lambda):
            if f.expr == f.variables[0]:
                return X.is_subset(Y) == True
        return False
    except Exception:
        return False

def is_continuous(f, X, Y):
    if hasattr(f, 'is_continuous'):
        return f.is_continuous(X, Y)
    if isinstance(f, dict) and f.get('type') == 'inclusion':
        return True
    try:
        if isinstance(f, Lambda):
            if f.expr == f.variables[0]:
                return True
        return False
    except Exception:
        return False

def is_open_map(f, X, Y):
    if hasattr(f, 'is_open_map'):
        return f.is_open_map(X, Y)
    if isinstance(f, dict) and f.get('type') == 'inclusion':
        return is_open_in_R(X)
    try:
        if isinstance(f, Lambda):
            if f.expr == f.variables[0]:
                return is_open_in_R(X)
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            X = witness.get('X')
            Y = witness.get('Y')
            f = witness.get('f')
        else:
            X, Y, f = witness
    except Exception:
        return [False] * 5

    try:
        h1 = is_metric_space(X) and is_metric_space(Y)
    except Exception:
        h1 = False

    try:
        h2 = is_locally_compact(X)
    except Exception:
        h2 = False

    try:
        h3 = is_valid_map(f, X, Y) and is_continuous(f, X, Y)
    except Exception:
        h3 = False

    try:
        h4 = is_open_map(f, X, Y)
    except Exception:
        h4 = False

    try:
        neg_q = not (is_metric_space(Y) and is_locally_compact(Y))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: X and Y are metric spaces",
    "H_2: X is locally compact",
    "H_3: f: X -> Y is a continuous map",
    "H_4: f is an open map",
    "¬Q: Y is not a locally compact metric space"
]

N_HYP = 4
NEG_Q_INDEX = 4
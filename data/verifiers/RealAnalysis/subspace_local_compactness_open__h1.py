import sympy
from sympy import S, Interval, Union, Intersection, FiniteSet, Complement
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings that the witness expression may reference
Q = S.Rationals
R = S.Reals
Z = S.Integers

def is_open_in(U, X):
    """Check if U is an open subset of X in the subspace topology from Reals."""
    if hasattr(U, 'is_open_in'):
        val = U.is_open_in
        if callable(val):
            try:
                return val(X)
            except Exception:
                pass
        return bool(val)

    if U == X:
        return True
    
    try:
        if not U.is_subset(X):
            return False
    except Exception:
        pass

    if X == S.Reals:
        try:
            if U.is_open:
                return True
        except Exception:
            pass
        return False

    if isinstance(U, Union):
        try:
            return all(is_open_in(arg, X) for arg in U.args)
        except Exception:
            return False

    if isinstance(U, Intersection):
        if X in U.args:
            other_args = [arg for arg in U.args if arg != X]
            if len(other_args) == 1:
                other = other_args[0]
            else:
                other = Intersection(*other_args)
            try:
                if other.is_open:
                    return True
            except Exception:
                pass
    
    try:
        if U.is_empty:
            return True
    except Exception:
        pass

    return False

def is_locally_compact(U):
    """Check if the space U is locally compact."""
    if hasattr(U, 'is_locally_compact'):
        val = U.is_locally_compact
        if callable(val):
            try:
                return val()
            except Exception:
                pass
        return bool(val)
        
    if hasattr(U, 'locally_compact'):
        val = U.locally_compact
        if callable(val):
            try:
                return val()
            except Exception:
                pass
        return bool(val)

    try:
        if U.is_empty:
            return True
    except Exception:
        pass

    if U == S.Reals or U == S.Integers:
        return True
    if U == S.Rationals:
        return False
    
    if isinstance(U, Complement):
        if U.args[0] == S.Reals and U.args[1] == S.Rationals:
            return False
        try:
            if is_locally_compact(U.args[0]) and isinstance(U.args[1], FiniteSet):
                return True
        except Exception:
            pass

    if isinstance(U, Interval):
        return True
    if isinstance(U, FiniteSet):
        return True
    if isinstance(U, Union):
        try:
            return all(is_locally_compact(arg) for arg in U.args)
        except Exception:
            return True
    if isinstance(U, Intersection):
        if S.Rationals in U.args:
            return False
        if Complement(S.Reals, S.Rationals) in U.args:
            return False

    try:
        if U.is_subset(S.Reals):
            if U.is_open or U.is_closed:
                return True
    except Exception:
        pass

    # Default to True to avoid false positives in neg_Q
    return True

def conditions(witness) -> list[bool]:
    # Extract X and U from the witness
    if isinstance(witness, dict):
        X = witness.get("X", witness.get("x"))
        U = witness.get("U", witness.get("u"))
        if X is None or U is None:
            try:
                X = U = list(witness.values())[0]
            except Exception:
                X = U = None
    elif isinstance(witness, tuple) and len(witness) == 2:
        X, U = witness
    else:
        X = witness
        U = witness

    # H_1: U is an open subset of X
    try:
        h1_ok = bool(is_open_in(U, X))
    except Exception:
        h1_ok = False

    # ¬Q: U is NOT locally compact
    try:
        neg_q_ok = not bool(is_locally_compact(U))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: U is an open subset of X",
    "¬Q: U is not locally compact"
]

N_HYP = 1
NEG_Q_INDEX = 1
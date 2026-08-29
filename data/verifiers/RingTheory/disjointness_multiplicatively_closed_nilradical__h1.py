import sympy
from sympy import eye, zeros, symbols, Rational, Integer, S
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
Z = S.Integers
Q = S.Rationals

def is_zero(val):
    """Safely check if a value is zero."""
    try:
        if hasattr(val, 'is_zero_matrix') and val.is_zero_matrix:
            return True
    except Exception:
        pass
    try:
        if hasattr(val, 'is_zero') and val.is_zero is True:
            return True
    except Exception:
        pass
    try:
        eq = (val == 0)
        if isinstance(eq, bool) and eq:
            return True
        if hasattr(eq, 'all') and eq.all():
            return True
    except Exception:
        pass
    try:
        from sympy import expand
        if expand(val) == 0:
            return True
    except Exception:
        pass
    return False

def in_S(val, S_list):
    """Safely check if a value is in the list S_list."""
    for c in S_list:
        try:
            eq = (val == c)
            if isinstance(eq, bool) and eq:
                return True
            if hasattr(eq, 'all') and eq.all():
                return True
        except Exception:
            pass
        try:
            if hasattr(val, 'equals') and val.equals(c):
                return True
        except Exception:
            pass
        try:
            from sympy import expand
            diff = val - c
            if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix:
                return True
            if expand(diff) == 0:
                return True
        except Exception:
            pass
    return False

def is_nilpotent(val, max_iter=50):
    """Check if an element is nilpotent by computing its powers."""
    try:
        if is_zero(val):
            return True
        curr = val
        for _ in range(max_iter):
            curr = curr * val
            if is_zero(curr):
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if it FAILS the conclusion (neg_Q is True).
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', None)
            S_obj = witness.get('S', witness)
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, S_obj = witness
        else:
            R = None
            S_obj = witness
    except Exception:
        R = None
        S_obj = witness

    try:
        S_list = list(S_obj)
    except Exception:
        return [False, False, False]

    # H_1: S is a multiplicatively closed subset of R
    h1 = True
    try:
        for a in S_list:
            for b in S_list:
                if not in_S(a * b, S_list):
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    # H_2: 0 is not an element of S
    h2 = True
    try:
        for val in S_list:
            if is_zero(val):
                h2 = False
                break
    except Exception:
        h2 = False

    # neg_Q: The intersection of S and the nilradical of R is not empty
    neg_q = False
    try:
        # If R is explicitly provided and has a nilradical attribute/method
        if R is not None and hasattr(R, 'nilradical'):
            nr = R.nilradical() if callable(R.nilradical) else R.nilradical
            if in_S(nr, S_list):
                neg_q = True
            else:
                for val in S_list:
                    try:
                        if val in nr:
                            neg_q = True
                            break
                    except Exception:
                        pass
        
        # Fallback: check if any element in S is nilpotent
        if not neg_q:
            for val in S_list:
                if is_nilpotent(val):
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: 0 is not an element of S",
    "¬Q: The intersection of S and the nilradical of R is not empty"
]

N_HYP = 2
NEG_Q_INDEX = 2
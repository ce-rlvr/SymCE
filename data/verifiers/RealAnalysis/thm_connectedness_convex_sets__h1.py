import sympy
from sympy import S, Interval, Intersection, FiniteSet

# Top-level setup
# Define some standard spaces and subsets that might be used as witnesses.
Q_space = S.Rationals
R_space = S.Reals
Q_interval = Intersection(Interval(0, 1), S.Rationals)
R_interval = Interval(0, 1)

def conditions(witness) -> list[bool]:
    # Extract C if witness is a tuple (V, C)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            V, C = witness
        else:
            C = witness
    except Exception:
        C = witness

    try:
        # H1: C is a convex subset of V
        h1 = False
        if isinstance(C, str):
            if C in ["Q", "Rationals", "Q_space", "R", "Reals", "R_space", "Q_interval", "R_interval"]:
                h1 = True
        elif C == S.Rationals or C == S.Reals or C == S.EmptySet:
            h1 = True
        elif isinstance(C, Interval):
            h1 = True
        elif isinstance(C, FiniteSet) and len(C) == 1:
            h1 = True
        elif isinstance(C, Intersection):
            if S.Rationals in C.args or S.Reals in C.args:
                others = [a for a in C.args if a not in (S.Rationals, S.Reals)]
                if len(others) == 1 and isinstance(others[0], Interval):
                    h1 = True
        elif hasattr(C, 'is_convex'):
            h1 = bool(C.is_convex())
    except Exception:
        h1 = False

    try:
        # Q: C is a connected topological space
        # neg_Q: C is NOT connected
        is_conn = True
        if isinstance(C, str):
            if C in ["Q", "Rationals", "Q_space", "Q_interval"]:
                is_conn = False
            elif C in ["R", "Reals", "R_space", "R_interval"]:
                is_conn = True
        elif C == S.Rationals:
            is_conn = False
        elif C == S.Reals or C == S.EmptySet:
            is_conn = True
        elif isinstance(C, Interval):
            is_conn = True
        elif isinstance(C, FiniteSet):
            is_conn = len(C) <= 1
        elif isinstance(C, Intersection):
            if S.Rationals in C.args:
                others = [a for a in C.args if a != S.Rationals]
                if len(others) == 1 and isinstance(others[0], Interval):
                    is_conn = (others[0].measure == 0)
            elif S.Reals in C.args:
                others = [a for a in C.args if a != S.Reals]
                if len(others) == 1 and isinstance(others[0], Interval):
                    is_conn = True
        elif hasattr(C, 'is_connected'):
            is_conn = bool(C.is_connected())
        
        neg_q = not is_conn
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: C is a convex subset of V",
    "¬Q: C is not a connected topological space"
]

N_HYP = 1
NEG_Q_INDEX = 1
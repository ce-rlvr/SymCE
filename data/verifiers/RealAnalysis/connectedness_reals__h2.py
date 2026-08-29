import sympy

EmptySet = sympy.S.EmptySet
Reals = sympy.S.Reals
R = sympy.S.Reals
Interval = sympy.Interval
Union = sympy.Union
Intersection = sympy.Intersection
FiniteSet = sympy.FiniteSet

def conditions(witness) -> list[bool]:
    # H1: S is a subset of the real numbers
    try:
        h1_val = witness.is_subset(sympy.S.Reals)
        h1 = False if h1_val is None else bool(h1_val)
    except Exception:
        h1 = False

    # H2: S is open
    try:
        if witness == sympy.S.EmptySet or witness == sympy.S.Reals:
            h2 = True
        elif isinstance(witness, sympy.Interval):
            h2 = bool(witness.left_open and witness.right_open)
        else:
            try:
                h2 = bool(witness.interior == witness)
            except Exception:
                h2 = False
    except Exception:
        h2 = False

    # H3: S is closed
    try:
        if witness == sympy.S.EmptySet or witness == sympy.S.Reals:
            h3 = True
        elif isinstance(witness, sympy.Interval):
            h3 = bool(not witness.left_open and not witness.right_open)
        else:
            try:
                h3 = bool(witness.closure == witness)
            except Exception:
                h3 = False
    except Exception:
        h3 = False

    # neg_Q: S is not equal to the set of all real numbers
    try:
        neg_q = bool(witness != sympy.S.Reals)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: S is a subset of the real numbers",
    "H_2: S is open",
    "H_3: S is closed",
    "¬Q: S is not equal to the set of all real numbers"
]

N_HYP = 3
NEG_Q_INDEX = 3
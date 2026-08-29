import sympy
from sympy import eye, Matrix
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_identity(val):
    if hasattr(val, 'is_Matrix') and val.is_Matrix:
        return eye(val.shape[0])
    return 1

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    Hypotheses:
      - R is a ring with identity 1
      - a is an element of R
      - There exists an element c in R such that ac = 1
    Conclusion:
      - a is a unit in R and b = c
    """
    # Extract witness components
    if isinstance(witness, dict):
        a = witness.get('a')
        c = witness.get('c')
        b = witness.get('b')
    elif hasattr(witness, 'a') and hasattr(witness, 'c'):
        a = getattr(witness, 'a', None)
        c = getattr(witness, 'c', None)
        b = getattr(witness, 'b', None)
    elif isinstance(witness, (list, tuple)):
        a = witness[0] if len(witness) > 0 else None
        c = witness[1] if len(witness) > 1 else None
        b = witness[2] if len(witness) > 2 else None
    else:
        a, c, b = None, None, None

    # H_1: R is a ring with identity 1
    try:
        ident = get_identity(a)
        h1 = ident is not None
    except Exception:
        h1 = False

    # H_2: a is an element of R
    # In a ring, elements must support addition and multiplication (closure).
    try:
        _ = a + a
        _ = a * a
        h2 = True
    except Exception:
        h2 = False

    # H_3: There exists an element c in R such that ac = 1
    try:
        ident = get_identity(a)
        h3 = bool(a * c == ident)
    except Exception:
        h3 = False

    # ¬Q: a is not a unit in R or b != c
    # If ac = 1, then a is a unit if and only if ca = 1 (c must be the two-sided inverse).
    try:
        ident = get_identity(a)
        is_unit_a = bool(c * a == ident)
        q = is_unit_a and bool(b == c)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity 1",
    "H_2: a is an element of R",
    "H_3: There exists an element c in R such that ac = 1",
    "¬Q: a is not a unit in R or b != c"
]

N_HYP = 3
NEG_Q_INDEX = 3
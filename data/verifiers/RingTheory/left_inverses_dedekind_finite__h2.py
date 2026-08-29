import sympy
from sympy import eye, zeros, simplify
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (a, b) or (R, a, b), checks if it is a valid counterexample to:
    Hypothesis: R is a Dedekind-finite ring.
    Conclusion: a is a unit in R, and b is its two-sided inverse such that ba = 1.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) >= 2:
                a, b = witness[-2], witness[-1]
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: a and b belong to a Dedekind-finite ring
    # In SymPy, all standard finite-dimensional matrices and scalars belong to Dedekind-finite rings.
    h1 = False
    try:
        if hasattr(a, 'is_Matrix') and a.is_Matrix and hasattr(b, 'is_Matrix') and b.is_Matrix:
            if a.shape == b.shape and a.shape[0] == a.shape[1]:
                h1 = True
        else:
            from sympy import Expr
            if isinstance(a, (int, float, complex, Expr)) and isinstance(b, (int, float, complex, Expr)):
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: It is NOT the case that (a is a unit and b is its two-sided inverse)
    # i.e., not (ab == 1 and ba == 1)
    neg_q = False
    try:
        ab = a * b
        ba = b * a

        def is_one(val):
            if hasattr(val, 'is_Matrix') and val.is_Matrix:
                return val == eye(val.shape[0])
            try:
                return bool(simplify(val - 1) == 0)
            except Exception:
                return val == 1

        ab_is_one = is_one(ab)
        ba_is_one = is_one(ba)

        neg_q = not (ab_is_one and ba_is_one)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Dedekind-finite ring containing a and b",
    "¬Q: a is not a unit with two-sided inverse b (i.e., ab != 1 or ba != 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1
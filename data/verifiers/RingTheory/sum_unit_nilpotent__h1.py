import sympy as sp
from sympy.matrices import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero(val):
    """Helper to check if a value is mathematically zero."""
    try:
        if val == 0:
            return True
        if hasattr(val, 'is_zero') and val.is_zero is True:
            return True
        return sp.simplify(val) == 0
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (u, x), checks if it is a valid counterexample to the conjecture:
    'In a ring R, the sum of a unit and a nilpotent element is a unit.'
    (This is false for non-commutative rings).
    """
    try:
        u, x = witness
    except Exception:
        return [False, False, False, False]

    # H_1: R has a multiplicative identity
    try:
        if hasattr(u, 'is_Matrix') and hasattr(x, 'is_Matrix'):
            # The ring of n x n matrices has an identity matrix
            h1_ok = bool(u.is_square and x.is_square and u.shape == x.shape)
        else:
            # If they can be added, assume they belong to a standard ring with identity
            _ = u + x
            h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: u is a unit in R
    try:
        if hasattr(u, 'is_Matrix') and u.is_Matrix:
            # For matrices over a field, it is a unit iff determinant is non-zero
            h2_ok = bool(u.is_square and not is_zero(u.det()))
        else:
            h2_ok = not is_zero(u)
    except Exception:
        h2_ok = False

    # H_3: x is a nilpotent element in R
    try:
        if hasattr(x, 'is_Matrix') and x.is_Matrix:
            # An n x n matrix is nilpotent iff its n-th power is the zero matrix
            n = x.shape[0]
            xn = x**n
            h3_ok = all(is_zero(e) for e in xn)
        else:
            h3_ok = is_zero(x)
    except Exception:
        h3_ok = False

    # ¬Q: u + x is NOT a unit in R
    try:
        ux = u + x
        if hasattr(ux, 'is_Matrix') and ux.is_Matrix:
            # It fails to be a unit if its determinant is zero
            neg_q_ok = bool(is_zero(ux.det()))
        else:
            neg_q_ok = bool(is_zero(ux))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: u is a unit in R",
    "H_3: x is a nilpotent element in R",
    "¬Q: u + x is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3
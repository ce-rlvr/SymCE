import sympy
from sympy.matrices import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample to the false conjecture.
    The witness should provide the linear transformation T, the linear functional f, and the vector w.
    Expected format: a tuple (T, f, w) or a dict with keys 'T', 'f', 'w' containing sympy Matrices.
    """
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            f = witness.get('f')
            w = witness.get('w')
        else:
            T, f, w = witness
    except Exception:
        return [False, False, False, False]

    # H_1: V and W are vector spaces over a field F
    # We verify this by checking that T, f, and w are represented as matrices.
    try:
        h1 = (hasattr(T, 'rows') and hasattr(T, 'cols') and
              hasattr(f, 'rows') and hasattr(f, 'cols') and
              hasattr(w, 'rows') and hasattr(w, 'cols'))
    except Exception:
        h1 = False

    # H_2: f is a linear functional in the dual space V*
    # f must be a 1 x n matrix, and its domain dimension (n) must match T's domain dimension.
    try:
        h2 = h1 and f.rows == 1 and f.cols == T.cols
    except Exception:
        h2 = False

    # H_3: w is a vector in W
    # w must be an m x 1 matrix, and its codomain dimension (m) must match T's codomain dimension.
    try:
        h3 = h1 and w.cols == 1 and w.rows == T.rows
    except Exception:
        h3 = False

    # ¬Q: The dual transformation T*: W* -> V* is given by T*(g) = g(w)f for all g in W*
    # This conclusion holds if and only if T = w * f.
    # The negated conclusion is that T != w * f.
    try:
        neg_q = False
        if h1 and h2 and h3:
            neg_q = bool(T != w * f)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F (T, f, w are matrices)",
    "H_2: f is a linear functional in the dual space V*",
    "H_3: w is a vector in W",
    "¬Q: The dual transformation T* is NOT given by T*(g) = g(w)f for all g"
]

N_HYP = 3
NEG_Q_INDEX = 3
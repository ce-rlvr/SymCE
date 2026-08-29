import sympy
from sympy.matrices import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should provide the linear transformation T and the bilinear form B.
    It can be a dictionary {'T': ..., 'B': ...} or a tuple (T, B).
    """
    try:
        if isinstance(witness, dict):
            T_raw = witness['T']
            B_raw = witness['B']
        else:
            T_raw = witness[0]
            B_raw = witness[1]
        T = Matrix(T_raw)
        B = Matrix(B_raw)
    except Exception:
        return [False, False, False]

    # H_1: V is a finite-dimensional vector space over a field F
    # We verify this by checking that T and B are valid square matrices of the same dimension > 0.
    try:
        h1 = bool(T.is_square and B.is_square and T.shape == B.shape and T.shape[0] > 0)
    except Exception:
        h1 = False

    # H_2: T is a linear transformation that is an isometry with respect to B
    # This means B(T(x), T(y)) = B(x, y) for all x, y, which is equivalent to T^T * B * T = B.
    try:
        diff = (T.transpose() * B * T) - B
        diff.simplify()
        h2 = bool(diff.is_zero_matrix)
    except Exception:
        h2 = False

    # neg_Q: The determinant of T is neither 1 nor -1
    try:
        det_T = T.det()
        if hasattr(det_T, 'simplify'):
            det_T = det_T.simplify()
        
        diff1 = sympy.simplify(det_T - 1)
        diff2 = sympy.simplify(det_T + 1)
        
        is_one = (diff1 == 0) or (getattr(diff1, 'is_zero', False) is True)
        is_minus_one = (diff2 == 0) or (getattr(diff2, 'is_zero', False) is True)
        
        neg_q = not (is_one or is_minus_one)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F (T and B are square matrices of same size)",
    "H_2: T is a linear transformation that is an isometry with respect to B",
    "¬Q: The determinant of T is neither 1 nor -1"
]

N_HYP = 2
NEG_Q_INDEX = 2
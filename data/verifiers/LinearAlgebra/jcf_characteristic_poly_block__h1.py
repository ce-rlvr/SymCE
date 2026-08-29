import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: J_m(\\lambda) is the m \\times m Jordan block with eigenvalue \\lambda",
    "¬Q: The characteristic polynomial of J_m(\\lambda) is not (x - \\lambda)^m"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture assumes the characteristic polynomial is defined as det(A - xI),
    which makes the conclusion (x - \lambda)^m false for odd m.
    """
    try:
        # Extract witness components
        if isinstance(witness, dict):
            m = witness.get('m')
            lambda_val = witness.get('lambda_val', witness.get('lambda'))
            J = witness.get('J')
            x = witness.get('x', sympy.Symbol('x'))
            if J is None and m is not None and lambda_val is not None:
                J = sympy.Matrix(m, m, lambda i, j: lambda_val if i == j else (1 if j == i + 1 else 0))
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                m, lambda_val = witness
                J = sympy.Matrix(m, m, lambda i, j: lambda_val if i == j else (1 if j == i + 1 else 0))
                x = sympy.Symbol('x')
            elif len(witness) == 3:
                m, lambda_val, J = witness
                x = sympy.Symbol('x')
            elif len(witness) == 4:
                m, lambda_val, J, x = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: m is a positive integer
    try:
        h1_ok = bool(isinstance(m, (int, sympy.Integer)) and m > 0)
    except Exception:
        h1_ok = False

    # H_2: J_m(\lambda) is the m \times m Jordan block with eigenvalue \lambda
    try:
        if not (hasattr(J, 'shape') and hasattr(J, 'det')):
            J = sympy.Matrix(J)
            
        if J.shape == (m, m):
            # Standard Jordan block (1s on superdiagonal)
            expected_J = sympy.Matrix(m, m, lambda i, j: lambda_val if i == j else (1 if j == i + 1 else 0))
            # Alternative convention (1s on subdiagonal)
            expected_J_sub = sympy.Matrix(m, m, lambda i, j: lambda_val if i == j else (1 if i == j + 1 else 0))
            
            diff1 = sympy.simplify(J - expected_J)
            diff2 = sympy.simplify(J - expected_J_sub)
            h2_ok = bool(diff1.is_zero_matrix or diff2.is_zero_matrix)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The characteristic polynomial of J_m(\lambda) is NOT (x - \lambda)^m
    try:
        if not h1_ok or not h2_ok:
            neg_q = False
        else:
            I = sympy.eye(m)
            # In contexts where this conjecture is false, the characteristic polynomial 
            # is defined as det(A - xI). We compute it and compare to (x - \lambda)^m.
            char_poly = (J - x*I).det()
            expected = (x - lambda_val)**m
            
            diff = sympy.simplify(char_poly - expected)
            neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]
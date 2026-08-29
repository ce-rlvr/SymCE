import sympy
from sympy import Matrix, eye, zeros, simplify
from sympy.abc import x
import math
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_m_i(M, lam):
    """
    Computes the size of the largest Jordan block corresponding to eigenvalue `lam` in matrix `M`.
    This is equivalent to the index of `lam` in `M`.
    """
    n = M.shape[0]
    if n == 0:
        return 0
    I = eye(n)
    B = M - lam * I
    prev_nullity = 0
    B_k = eye(n)
    for k in range(1, n + 2):
        B_k = B_k * B
        nullity = n - B_k.rank()
        if nullity == prev_nullity:
            return k - 1
        prev_nullity = nullity
    return n

def conditions(witness) -> list[bool]:
    # Extract A and J from the witness
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            J = witness.get('J')
        elif hasattr(witness, 'A') and hasattr(witness, 'J'):
            A = witness.A
            J = witness.J
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            A, J = witness
        else:
            A, J = witness, None
    except Exception:
        return [False, False]

    # H_1: A is a square matrix over the complex numbers
    h1_ok = False
    try:
        if isinstance(A, Matrix) and A.is_square:
            h1_ok = True
    except Exception:
        pass

    # ¬Q: The minimal polynomial of A is NOT the product of (x - lambda_i)^m_i
    # where m_i is the size of the largest Jordan block corresponding to lambda_i in J.
    neg_q_ok = False
    try:
        if J is not None and isinstance(J, Matrix) and J.is_square:
            eigenvals = list(A.eigenvals().keys())
            poly_prod = 1
            for lam in eigenvals:
                m_i = get_m_i(J, lam)
                poly_prod *= (x - lam)**m_i
            
            min_poly = A.minimal_polynomial(x)
            
            # Check if the minimal polynomial differs from the constructed product
            diff = simplify(min_poly - poly_prod)
            if diff != 0:
                neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is a square matrix over the complex numbers",
    "¬Q: The minimal polynomial of A is not the product of (x - lambda_i)^m_i based on J"
]

N_HYP = 1
NEG_Q_INDEX = 1
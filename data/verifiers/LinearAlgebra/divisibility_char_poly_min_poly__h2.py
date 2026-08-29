import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.matrices.matrixbase import MatrixBase
from sympy.abc import x

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # The witness can be just the matrix A, or a tuple (A, m_poly)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, m_poly = witness
        else:
            A = witness
            m_poly = None
    except Exception:
        A = witness
        m_poly = None

    # H_1: Let A be an n x n matrix over a field F
    try:
        h1 = isinstance(A, MatrixBase) and A.is_square
    except Exception:
        h1 = False

    # H_2: Let m(x) be the minimal polynomial of A
    try:
        if h1:
            actual_m = A.minimal_polynomial(x)
            if m_poly is not None:
                if hasattr(m_poly, 'as_expr'):
                    m_poly_expr = m_poly.as_expr()
                else:
                    m_poly_expr = m_poly
                h2 = sympy.simplify(actual_m - m_poly_expr) == 0
                m_poly = m_poly_expr
            else:
                m_poly = actual_m
                h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The minimal polynomial m(x) does NOT divide the characteristic polynomial p(x)
    try:
        if h1 and h2:
            p = A.charpoly(x).as_expr()
            rem = sympy.rem(p, m_poly, x)
            neg_q = sympy.simplify(rem) != 0
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field F",
    "H_2: m(x) is the minimal polynomial of A",
    "¬Q: m(x) does not divide the characteristic polynomial p(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2
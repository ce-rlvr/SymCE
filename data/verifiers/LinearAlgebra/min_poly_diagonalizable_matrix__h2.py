import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x
from sympy import factor_list

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    """
    # H_1: V is a finite-dimensional vector space over a field F.
    # We interpret this as the witness being a square matrix.
    try:
        h1 = isinstance(witness, sympy.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # H_2: T is diagonalizable over F.
    try:
        h2 = witness.is_diagonalizable()
    except Exception:
        h2 = False

    # ¬Q: The minimal polynomial of T does NOT factor completely over F 
    # into a product of distinct linear factors.
    try:
        minpoly = witness.minimal_polynomial(x)
        factors = factor_list(minpoly)[1]
        
        is_distinct_linear = True
        for fac, mult in factors:
            if mult > 1:
                is_distinct_linear = False
                break
            if fac.as_poly(x).degree() > 1:
                is_distinct_linear = False
                break
                
        neg_q = not is_distinct_linear
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: T is diagonalizable over F",
    "¬Q: The minimal polynomial of T does not factor completely over F into a product of distinct linear factors"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import eye, zeros
import math

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is a square matrix
    try:
        if not isinstance(witness, sympy.MatrixBase):
            matrix = sympy.Matrix(witness)
        else:
            matrix = witness
        h1 = matrix.is_square
    except Exception:
        h1 = False

    # neg_Q: There exist i, j such that |a_{ij}| > \sqrt{a_{ii} a_{jj}}
    neg_q = False
    try:
        if h1:
            n = matrix.rows
            for i in range(n):
                for j in range(n):
                    aii = complex(matrix[i, i])
                    ajj = complex(matrix[j, j])
                    aij = complex(matrix[i, j])
                    
                    prod = aii * ajj
                    # If the product of diagonal elements is negative or complex, 
                    # the square root is not a non-negative real number, making the 
                    # inequality |a_{ij}| <= \sqrt{a_{ii} a_{jj}} undefined/false.
                    if abs(prod.imag) > 1e-9 or prod.real < -1e-9:
                        neg_q = True
                        break
                    
                    sqrt_prod = math.sqrt(max(0.0, prod.real))
                    if abs(aij) > sqrt_prod + 1e-9:
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: There exist i, j such that |a_{ij}| > \\sqrt{a_{ii} a_{jj}}"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
import sympy.matrices
from sympy.matrices import Matrix, eye, zeros

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
I = sympy.I

def conditions(witness) -> list[bool]:
    # H_1: Let A be an n \times n matrix over the complex numbers
    try:
        h1 = bool(isinstance(witness, sympy.matrices.MatrixBase) and witness.is_square)
    except Exception:
        h1 = False

    # neg_Q: Not all coefficients of the characteristic polynomial of A are real numbers
    try:
        poly = witness.charpoly()
        coeffs = poly.all_coeffs()
        neg_q = False
        for c in coeffs:
            imag_part = sympy.im(sympy.expand_complex(c)).simplify()
            if imag_part != 0:
                if imag_part.is_number:
                    if abs(complex(imag_part)) > 1e-12:
                        neg_q = True
                        break
                else:
                    # If it's symbolic and doesn't simplify to 0, we assume it's non-zero
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over the complex numbers",
    "¬Q: The characteristic polynomial of A has at least one non-real coefficient"
]

N_HYP = 1
NEG_Q_INDEX = 1
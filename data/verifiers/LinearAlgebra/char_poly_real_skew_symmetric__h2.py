import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an n x n matrix with real entries
    try:
        if not isinstance(witness, sympy.MatrixBase):
            A = sympy.Matrix(witness)
        else:
            A = witness
            
        h1 = A.is_square
        if h1:
            for e in A:
                try:
                    if abs(complex(e).imag) > 1e-9:
                        h1 = False
                        break
                except Exception:
                    if e.is_real is not True:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # ¬Q: The characteristic polynomial of A has at least one root with a non-zero real part
    try:
        if not isinstance(witness, sympy.MatrixBase):
            A = sympy.Matrix(witness)
        else:
            A = witness
            
        x = sympy.Symbol('x')
        p = A.charpoly(x)
        roots = sympy.nroots(p)
        neg_q = False
        for r in roots:
            if abs(complex(r).real) > 1e-9:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a square matrix with real entries",
    "¬Q: The characteristic polynomial of A has at least one root with a non-zero real part"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: V is a vector space
    try:
        if isinstance(witness, list):
            witness = Matrix(witness)
        # A matrix implicitly defines a vector space F^n
        h1 = isinstance(witness, sympy.matrices.MatrixBase)
    except Exception:
        h1 = False

    # H_2: B is a bilinear form on V
    try:
        if isinstance(witness, list):
            witness = Matrix(witness)
        # A square matrix represents a bilinear form on F^n
        h2 = h1 and witness.is_square
    except Exception:
        h2 = False

    # ¬Q: B is neither symmetric nor alternating
    try:
        if isinstance(witness, list):
            witness = Matrix(witness)
            
        if not (isinstance(witness, sympy.matrices.MatrixBase) and witness.is_square):
            neg_q = False
        else:
            is_sym = witness.is_symmetric()
            
            is_alt = True
            if witness != -witness.T:
                is_alt = False
            else:
                for i in range(witness.rows):
                    if witness[i, i] != 0:
                        is_alt = False
                        break
            
            neg_q = (not is_sym) and (not is_alt)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: B is a bilinear form on V",
    "¬Q: B is neither symmetric nor alternating"
]

N_HYP = 2
NEG_Q_INDEX = 2
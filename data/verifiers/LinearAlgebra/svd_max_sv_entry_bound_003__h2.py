import sympy
from sympy import eye, zeros
from sympy.matrices.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, MatrixBase):
            h1 = False
        else:
            h1 = all(e.is_complex for e in witness)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, MatrixBase) or witness.rows == 0 or witness.cols == 0:
            neg_q = False
        else:
            max_elem = max(sympy.re(abs(e).evalf()) for e in witness)
            try:
                svs = witness.singular_values()
                max_sv = max(sympy.re(sv.evalf()) for sv in svs)
            except Exception:
                M = (witness.H * witness).evalf()
                evs = M.eigenvals().keys()
                max_sv = sympy.sqrt(max(sympy.re(e.evalf()) for e in evs))
            
            val_sv = sympy.re(max_sv.evalf())
            if val_sv.is_number and max_elem.is_number:
                # Use a small tolerance to avoid false positives from floating point inaccuracies
                neg_q = bool(val_sv < max_elem - 1e-12)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m \\times n matrix over the complex numbers",
    "¬Q: The maximum singular value of A is strictly less than the absolute value of some entry |a_{ij}|"
]

N_HYP = 1
NEG_Q_INDEX = 1
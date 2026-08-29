import sympy
from sympy import Matrix, I, eye, zeros
from sympy.matrices.matrixbase import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, MatrixBase):
            neg_q = False
        else:
            # A real matrix always has a real SVD.
            # A matrix with non-real or infinite entries cannot be written as 
            # the product of real orthogonal and real diagonal matrices.
            is_real_and_finite = True
            for e in witness:
                if e.is_real is False or e.has(I):
                    is_real_and_finite = False
                    break
                if e.is_finite is False:
                    is_real_and_finite = False
                    break
            
            neg_q = not is_real_and_finite
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: A does not have a real SVD (e.g., A is not a real matrix)"
]

N_HYP = 0
NEG_Q_INDEX = 0
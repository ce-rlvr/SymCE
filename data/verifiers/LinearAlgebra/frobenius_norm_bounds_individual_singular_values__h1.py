import sympy
from sympy import Matrix, eye, zeros, MatrixBase

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    neg_q = False
    if h1:
        try:
            norm_F = witness.norm()
            sigmas = witness.singular_values()
            for sigma in sigmas:
                try:
                    if bool(sigma > norm_F):
                        neg_q = True
                        break
                except TypeError:
                    try:
                        if bool(sigma.evalf() > norm_F.evalf()):
                            neg_q = True
                            break
                    except Exception:
                        pass
        except Exception:
            pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a matrix",
    "¬Q: There exists a singular value strictly greater than the Frobenius norm"
]

N_HYP = 1
NEG_Q_INDEX = 1
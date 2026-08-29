import sympy
from sympy import Matrix, eye, zeros, im, simplify
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, (list, tuple)):
            witness = Matrix(witness)
    except Exception:
        pass

    try:
        h1_ok = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1_ok = False

    try:
        h2_ok = h1_ok and all(entry.is_real == True for entry in witness)
    except Exception:
        h2_ok = False

    try:
        if not h1_ok or not h2_ok:
            neg_q_ok = False
        else:
            eigenvalues = witness.eigenvals()
            neg_q_ok = True
            for ev in eigenvalues:
                if ev.is_real == True:
                    neg_q_ok = False
                    break
                if simplify(im(ev)) == 0:
                    neg_q_ok = False
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over the field of real numbers",
    "H_2: T is a linear operator on V",
    "¬Q: T has no 1-dimensional invariant subspace (no real eigenvalues)"
]

N_HYP = 2
NEG_Q_INDEX = 2
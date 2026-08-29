import sympy
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not hasattr(witness, 'shape'):
            witness = Matrix(witness)
    except Exception:
        pass

    # H_1: Q is an orthogonal matrix
    try:
        n = witness.shape[0]
        if witness.shape[0] != witness.shape[1]:
            h1 = False
        else:
            diff = witness.T * witness - eye(n)
            try:
                h1 = all(abs(complex(diff[i, j])) < 1e-9 for i in range(n) for j in range(n))
            except TypeError:
                h1 = diff.expand() == zeros(n)
    except Exception:
        h1 = False

    # H_2: The determinant of Q is equal to 1
    try:
        d = witness.det()
        try:
            h2 = abs(complex(d) - 1.0) < 1e-9
        except TypeError:
            h2 = sympy.simplify(d - 1) == 0
    except Exception:
        h2 = False

    # ¬Q: The trace of Q is not equal to 1 + 2cos(θ) for any real θ
    try:
        tr = witness.trace()
        try:
            tr_c = complex(tr)
            if abs(tr_c.imag) > 1e-9:
                neg_q = True
            else:
                neg_q = tr_c.real < -1 - 1e-9 or tr_c.real > 3 + 1e-9
        except TypeError:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an orthogonal matrix",
    "H_2: The determinant of Q is equal to 1",
    "¬Q: The trace of Q is not equal to 1 + 2cos(θ) for any real θ"
]

N_HYP = 2
NEG_Q_INDEX = 2
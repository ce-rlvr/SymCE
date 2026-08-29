import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, Matrix):
            h1 = False
        elif witness.rows != witness.cols:
            h1 = False
        else:
            h1 = bool(witness * witness == witness)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, Matrix) or witness.rows != witness.cols:
            neg_q = False
        else:
            eigenvals = witness.eigenvals()
            if not eigenvals:
                neg_q = True
            else:
                max_val = -1.0
                for ev in eigenvals.keys():
                    try:
                        val = float(sympy.Abs(ev).evalf())
                        if val > max_val:
                            max_val = val
                    except Exception:
                        pass
                if max_val < -0.5:
                    neg_q = False
                else:
                    neg_q = abs(max_val - 1.0) > 1e-7
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a projection matrix",
    "¬Q: The spectral radius of P is not equal to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
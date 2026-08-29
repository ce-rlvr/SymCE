import sympy
from sympy import Matrix, eye, zeros, sympify
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            lmbda = witness.get('lambda', witness.get('lmbda'))
        else:
            T, lmbda = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = isinstance(T, MatrixBase) and T.is_square and T.shape[0] > 0
    except Exception:
        h1_ok = False

    try:
        h2_ok = False
        if h1_ok and T == T.H:
            evals = T.eigenvals().keys()
            pos_def = True
            for e in evals:
                if e.is_positive is True:
                    continue
                elif e.is_positive is False:
                    pos_def = False
                    break
                else:
                    if not (e.evalf() > 0):
                        pos_def = False
                        break
            h2_ok = pos_def
    except Exception:
        h2_ok = False

    try:
        l_sym = sympify(lmbda)
        if l_sym.is_real is False:
            is_pos_real = False
        else:
            try:
                is_pos_real = bool(l_sym > 0)
            except TypeError:
                is_pos_real = False
    except Exception:
        is_pos_real = False

    neg_q_ok = not is_pos_real

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "H_2: T is a positive definite self-adjoint linear operator on V",
    "¬Q: lambda is not a strictly positive real number"
]

N_HYP = 2
NEG_Q_INDEX = 2
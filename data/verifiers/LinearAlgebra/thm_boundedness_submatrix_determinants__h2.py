import sympy
from sympy import Matrix, eye, zeros, Abs, simplify, I, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            U = Matrix(witness['U'])
            M = Matrix(witness['M'])
        elif hasattr(witness, 'U') and hasattr(witness, 'M'):
            U = Matrix(witness.U)
            M = Matrix(witness.M)
        else:
            U, M = witness
            U = Matrix(U)
            M = Matrix(M)
    except Exception:
        return [False, False]

    h1_ok = False
    try:
        if U.rows == U.cols and U.rows > 0:
            n = U.rows
            diff = U * U.adjoint() - eye(n)
            is_zero = True
            for i in range(n):
                for j in range(n):
                    try:
                        val = float(Abs(diff[i, j]).evalf())
                        if val > 1e-9:
                            is_zero = False
                            break
                    except TypeError:
                        if simplify(diff[i, j]) != 0:
                            is_zero = False
                            break
                if not is_zero:
                    break
            h1_ok = is_zero
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if M.rows == M.cols and M.rows > 0:
            d = M.det()
            try:
                val = float(Abs(d).evalf())
                neg_q_ok = val > 1.0 + 1e-9
            except TypeError:
                pass
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: U is an n x n unitary matrix",
    "¬Q: The absolute value of the determinant of M is strictly greater than 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
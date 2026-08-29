import sympy
from sympy import Matrix, eye, zeros, simplify, expand, I

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, Matrix):
            W = Matrix(witness)
        else:
            W = witness
        h1 = W.rows == W.cols and W.rows > 0
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = W.rows
            prod = W * W.H
            diff = prod - eye(n)
            is_unitary = True
            for i in range(n):
                for j in range(n):
                    val = simplify(expand(diff[i, j]))
                    if val != 0:
                        is_unitary = False
                        break
                if not is_unitary:
                    break
            # If U is not unitary, it cannot have a unitary square root.
            # If U is unitary, it always has a unitary square root.
            # Thus, the non-existence of a unitary square root is equivalent to U not being unitary.
            neg_q = not is_unitary
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n complex matrix",
    "¬Q: There does not exist a unitary matrix V such that V^2 = U"
]

N_HYP = 1
NEG_Q_INDEX = 1
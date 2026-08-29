import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: V is a finite-dimensional inner product space
    # We interpret the witness as an operator U on V, represented by a square matrix.
    try:
        if not isinstance(witness, Matrix):
            W = Matrix(witness)
        else:
            W = witness
        h1 = W.is_square
    except Exception:
        h1 = False

    # neg_Q: The conclusion FAILS at the witness.
    # Conclusion: For all x in V, ||Ux|| = ||x|| (i.e., U is an isometry, U^H U = I).
    # Negated Conclusion: U is NOT an isometry (U^H U != I).
    try:
        if not h1:
            neg_q = False
        else:
            n = W.shape[0]
            diff = W.H * W - eye(n)
            is_zero = True
            for i in range(n):
                for j in range(n):
                    if sympy.simplify(diff[i, j]) != 0:
                        is_zero = False
                        break
                if not is_zero:
                    break
            neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space (witness is a square matrix)",
    "¬Q: U is not an isometry (U^H U != I)"
]

N_HYP = 1
NEG_Q_INDEX = 1
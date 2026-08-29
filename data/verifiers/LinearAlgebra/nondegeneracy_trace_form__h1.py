import sympy
from sympy import Matrix, eye, zeros

# Standard bindings that might be useful for matrix witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a list or tuple of sympy.Matrix objects that form a basis
    for a vector space V of matrices.
    """
    # H_1: Witness is a non-empty list of square matrices of the same size
    try:
        h1 = (isinstance(witness, (list, tuple)) and len(witness) > 0 and
              all(isinstance(m, Matrix) for m in witness) and
              all(m.is_square for m in witness) and
              len(set(m.shape for m in witness)) == 1)
    except Exception:
        h1 = False

    # H_2: The matrices form a basis for V (they are linearly independent)
    try:
        if h1:
            flattened = [list(m) for m in witness]
            M = Matrix(flattened)
            h2 = M.rank() == len(witness)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The trace form B(X,Y) = Tr(XY) is degenerate on V
    # This happens if and only if the Gram matrix of the form has determinant 0.
    try:
        if h1 and h2:
            n = len(witness)
            G = zeros(n, n)
            for i in range(n):
                for j in range(n):
                    G[i, j] = (witness[i] * witness[j]).trace()
            det_val = sympy.simplify(G.det())
            neg_q = bool(det_val == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a space of square matrices (witness is a non-empty list of matrices of the same size)",
    "H_2: The matrices in the witness are linearly independent (forming a basis for V)",
    "¬Q: The trace form B(X,Y) = Tr(XY) is degenerate on V"
]

N_HYP = 2
NEG_Q_INDEX = 2
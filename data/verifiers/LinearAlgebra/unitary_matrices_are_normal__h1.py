import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, sympy.MatrixBase):
            return [False, False]
    except Exception:
        return [False, False]

    try:
        # H_1: U is a unitary matrix
        # In the context of a dropped "square matrix" hypothesis, 
        # a rectangular matrix with orthonormal columns or rows satisfies this.
        h1 = bool((witness.H * witness == sympy.eye(witness.cols)) or 
                  (witness * witness.H == sympy.eye(witness.rows)))
    except Exception:
        h1 = False

    try:
        # ¬Q: U is not a normal matrix
        # U commutes with its conjugate transpose means U * U.H == U.H * U.
        # For rectangular matrices, these products have different dimensions and cannot be equal.
        neg_q = bool(witness * witness.H != witness.H * witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "¬Q: U is not a normal matrix (does not commute with its conjugate transpose)"
]

N_HYP = 1
NEG_Q_INDEX = 1
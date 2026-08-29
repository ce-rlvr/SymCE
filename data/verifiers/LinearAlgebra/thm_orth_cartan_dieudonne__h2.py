import sympy
from sympy import MatrixBase, eye, im, simplify
from sympy.matrices import zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: Let Q be an n x n real matrix
    try:
        h1_ok = isinstance(witness, MatrixBase) and witness.rows == witness.cols
        if h1_ok:
            for e in witness:
                if e.is_real is False:
                    h1_ok = False
                    break
                elif e.is_real is None:
                    if simplify(im(e)) != 0:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # ¬Q: Q cannot be factored into a product of at most n Householder reflection matrices.
    # Householder reflections are orthogonal matrices, and the product of orthogonal matrices is orthogonal.
    # Thus, if Q is not orthogonal, it cannot be factored into any number of Householder reflections.
    # By the Cartan-Dieudonné theorem, if Q is orthogonal, it CAN be factored into at most n reflections.
    # Therefore, the conclusion fails if and only if Q is not an orthogonal matrix.
    try:
        if not (isinstance(witness, MatrixBase) and witness.rows == witness.cols):
            neg_q_ok = False
        else:
            n = witness.rows
            diff = witness.T * witness - eye(n)
            is_orthogonal = True
            for e in diff:
                if simplify(e) != 0:
                    is_orthogonal = False
                    break
            neg_q_ok = not is_orthogonal
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Q is an n x n real matrix",
    "¬Q: Q cannot be factored into a product of at most n Householder reflection matrices"
]

N_HYP = 1
NEG_Q_INDEX = 1
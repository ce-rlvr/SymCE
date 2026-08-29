import sympy as sp
from sympy import MatrixBase, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that S is a linear transformation from V to W.
    A valid counterexample will have S and T as matrices with incompatible dimensions,
    making the composition ST undefined, and thus (ST)^* != T^* S^*.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                S, T = witness
            elif len(witness) == 5:
                U, V, W, S, T = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        # Convert to sympy matrices if they are lists/tuples
        if not isinstance(S, MatrixBase):
            S = sp.Matrix(S)
        if not isinstance(T, MatrixBase):
            T = sp.Matrix(T)
    except Exception:
        return [False, False, False]

    # H_1: U, V, and W are finite-dimensional inner product spaces
    # Represented by the fact that S and T are finite-dimensional matrices
    try:
        h1 = isinstance(S, MatrixBase) and isinstance(T, MatrixBase)
    except Exception:
        h1 = False

    # H_2: T is a linear transformation from U to V
    # Represented by T being a valid matrix
    try:
        h2 = isinstance(T, MatrixBase)
    except Exception:
        h2 = False

    # ¬Q: (ST)^* != T^* S^*
    # If dimensions are incompatible (because S is not from V to W), 
    # S*T will raise an exception, meaning the equality fails.
    try:
        lhs = (S * T).adjoint()
        rhs = T.adjoint() * S.adjoint()
        eq = (lhs == rhs)
    except Exception:
        eq = False

    neg_q = not eq

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: U, V, and W are finite-dimensional inner product spaces",
    "H_2: T is a linear transformation from U to V",
    "¬Q: (ST)^* != T^* S^*"
]

N_HYP = 2
NEG_Q_INDEX = 2
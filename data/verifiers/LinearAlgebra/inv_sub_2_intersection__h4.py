import sympy
from sympy import Matrix, eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    Hypotheses:
      H1: V is a vector space
      H2: T is a linear operator on V
      H3: U is a T-invariant subspace of V
    Conclusion:
      Q: The intersection U \cap W is a T-invariant subspace of V.
    
    The witness should provide T, U, and W.
    """
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            U = witness.get('U')
            W = witness.get('W')
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            T, U, W = witness
        else:
            return [False, False, False, False]
            
        h1 = False
        if isinstance(T, (list, tuple)):
            T = Matrix(T)
            
        if isinstance(T, Matrix) and T.is_square:
            dim = T.rows
            h1 = True
            
            # Process U
            if isinstance(U, Matrix):
                U = [U[:, i] for i in range(U.cols)]
            elif not isinstance(U, (list, tuple)):
                h1 = False
            else:
                new_U = []
                for v in U:
                    if isinstance(v, (list, tuple)):
                        v = Matrix(v)
                        if v.shape[1] != 1:
                            v = v.reshape(len(v), 1)
                    if not isinstance(v, Matrix) or v.shape != (dim, 1):
                        h1 = False
                        break
                    new_U.append(v)
                U = new_U

            # Process W
            if isinstance(W, Matrix):
                W = [W[:, i] for i in range(W.cols)]
            elif not isinstance(W, (list, tuple)):
                h1 = False
            else:
                new_W = []
                for v in W:
                    if isinstance(v, (list, tuple)):
                        v = Matrix(v)
                        if v.shape[1] != 1:
                            v = v.reshape(len(v), 1)
                    if not isinstance(v, Matrix) or v.shape != (dim, 1):
                        h1 = False
                        break
                    new_W.append(v)
                W = new_W
    except Exception:
        h1 = False

    # H2: T is a linear operator on V (implicitly checked by T being a square matrix matching V's dimension)
    try:
        h2 = h1
    except Exception:
        h2 = False

    # H3: U is a T-invariant subspace of V
    try:
        h3 = False
        if h1:
            if not U:
                h3 = True
            else:
                M_U = Matrix.hstack(*U)
                rank_U = M_U.rank()
                h3 = True
                for v in U:
                    Tv = T * v
                    if Matrix.hstack(M_U, Tv).rank() > rank_U:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # ¬Q: The intersection U \cap W is NOT a T-invariant subspace of V
    try:
        neg_q = False
        if h1:
            if not U or not W:
                int_basis = []
            else:
                M_U = Matrix.hstack(*U)
                M_W = Matrix.hstack(*W)
                if M_U.cols == 0 or M_W.cols == 0:
                    int_basis = []
                else:
                    # Find intersection by solving [M_U, -M_W] * [x; y] = 0
                    B = Matrix.hstack(M_U, -M_W)
                    null_basis = B.nullspace()
                    int_basis = []
                    for n in null_basis:
                        x = n[:M_U.cols, :]
                        v = M_U * x
                        if not all(val == 0 for val in v):
                            int_basis.append(v)
            
            if not int_basis:
                is_inv = True
            else:
                M_int = Matrix.hstack(*int_basis)
                rank_int = M_int.rank()
                is_inv = True
                for v in int_basis:
                    Tv = T * v
                    if Matrix.hstack(M_int, Tv).rank() > rank_int:
                        is_inv = False
                        break
            neg_q = not is_inv
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: T is a linear operator on V",
    "H_3: U is a T-invariant subspace of V",
    "¬Q: The intersection U \\cap W is not a T-invariant subspace of V"
]

N_HYP = 3
NEG_Q_INDEX = 3
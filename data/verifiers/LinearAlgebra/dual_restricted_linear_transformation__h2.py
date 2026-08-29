import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices.matrixbase import MatrixBase

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (T, U) where:
      - T is an n x n sympy Matrix representing the linear transformation on V = F^n.
      - U is an n x k sympy Matrix whose columns span the subspace U.
    """
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            U = witness.get('U')
        elif isinstance(witness, tuple) or isinstance(witness, list):
            T = witness[0]
            U = witness[1]
        else:
            T = witness.T
            U = witness.U
    except Exception:
        return [False, False, False, False]

    # H_1: V is a vector space over a field F, U is a subspace
    try:
        h1 = isinstance(T, MatrixBase) and isinstance(U, MatrixBase) and \
             T.is_square and T.rows == U.rows
    except Exception:
        h1 = False

    # H_2: U is a subspace of V that is invariant under T
    try:
        if h1:
            _, col_pivots = U.rref()
            if len(col_pivots) == 0:
                h2 = True  # The zero subspace is always invariant
            else:
                U_basis = U[:, col_pivots]
                aug = U_basis.row_join(T * U_basis)
                h2 = (U_basis.rank() == aug.rank())
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: i: U -> V is the natural inclusion map
    # In our matrix representation, U_basis itself acts as the inclusion map from F^k to F^n.
    h3 = h1

    # Conclusion: (T|_U)* \circ i* = i* \circ T*
    try:
        if h1 and h2:
            _, col_pivots = U.rref()
            if len(col_pivots) == 0:
                q = True
            else:
                U_basis = U[:, col_pivots]
                
                # Find the restriction of T to U, denoted T_U
                # We need T_U such that U_basis * T_U = T * U_basis
                # Extract a non-singular k x k submatrix from U_basis to solve for T_U
                _, row_pivots = U_basis.T.rref()
                U_sub = U_basis[row_pivots, :]
                TU_sub = (T * U_basis)[row_pivots, :]
                
                T_U = U_sub.inv() * TU_sub
                
                # The dual of a map represented by matrix M is M.T
                # i* is U_basis.T, T* is T.T, (T|_U)* is T_U.T
                left_side = T_U.T * U_basis.T
                right_side = U_basis.T * T.T
                
                diff = left_side - right_side
                diff.simplify()
                q = all(val == 0 for val in diff)
        else:
            q = True
    except Exception:
        q = True

    neg_q = not q

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: U is a subspace of V that is invariant under T",
    "H_3: i: U -> V is the natural inclusion map",
    "¬Q: (T|_U)* \\circ i* != i* \\circ T*"
]

N_HYP = 3
NEG_Q_INDEX = 3
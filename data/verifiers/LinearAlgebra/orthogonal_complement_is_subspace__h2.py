import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is an inner product space",
    "¬Q: The orthogonal complement S^\\perp is not a subspace of V"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    V = None
    S = None
    
    # Extract V and S from the witness
    try:
        if isinstance(witness, dict):
            V = witness.get('V', witness.get('v'))
            S = witness.get('S', witness.get('s'))
        elif hasattr(witness, 'V') and hasattr(witness, 'S'):
            V = witness.V
            S = witness.S
        elif hasattr(witness, 'v') and hasattr(witness, 's'):
            V = witness.v
            S = witness.s
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            V = witness[0]
            S = witness[1]
    except Exception:
        pass

    def to_matrix(X):
        if isinstance(X, sympy.MatrixBase):
            return X
        if isinstance(X, (list, tuple)):
            if len(X) == 0:
                return None
            if isinstance(X[0], sympy.MatrixBase):
                return sympy.Matrix.hstack(*X)
            elif isinstance(X[0], (list, tuple)):
                return sympy.Matrix(X)
            elif isinstance(X[0], (int, float, complex, sympy.Expr)):
                return sympy.Matrix(X)
        return None

    try:
        V_mat = to_matrix(V)
        S_mat = to_matrix(S)
    except Exception:
        V_mat = None
        S_mat = None

    # H_1: V is an inner product space
    # Any valid matrix represents a vector space (its column space) over R or C, 
    # which naturally forms an inner product space.
    h1 = False
    try:
        if V_mat is not None:
            h1 = True
    except Exception:
        pass

    # ¬Q: S^\perp is NOT a subspace of V
    neg_q = False
    try:
        if V_mat is not None and S_mat is not None:
            if V_mat.rows != S_mat.rows:
                # If they are in different ambient spaces, S^\perp cannot be a subspace of V
                neg_q = True
            else:
                # Compute S^\perp in the ambient space (nullspace of the conjugate transpose)
                S_perp_basis = S_mat.H.nullspace()
                
                # Check if S^\perp is a subspace of V
                # i.e., every basis vector of S^\perp must be in the column space of V
                is_subspace = True
                rank_V = V_mat.rank()
                for u in S_perp_basis:
                    # If appending u increases the rank, u is not in the column space of V
                    if V_mat.row_join(u).rank() > rank_V:
                        is_subspace = False
                        break
                
                neg_q = not is_subspace
    except Exception:
        pass

    return [h1, neg_q]
import sympy as sp
from sympy import Matrix, zeros, eye

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    'Preservation of Orthogonal Complements under Bijective Isometries'
    (with the bijective isometry hypothesis dropped).
    """
    try:
        B_V = witness['B_V']
        B_W = witness['B_W']
        U = witness['U']
        T = witness['T']
    except Exception:
        return [False, False, False]

    # H_1: V and W are vector spaces equipped with symmetric bilinear forms B_V and B_W respectively
    try:
        h1 = (B_V.shape[0] == B_V.shape[1] and 
              B_W.shape[0] == B_W.shape[1] and 
              B_V == B_V.T and B_W == B_W.T)
    except Exception:
        h1 = False

    # H_2: U is a subspace of V, and T is a linear map from V to W
    try:
        h2 = (U.shape[0] == B_V.shape[0] and 
              T.shape[0] == B_W.shape[0] and T.shape[1] == B_V.shape[0])
    except Exception:
        h2 = False

    # ¬Q: The image of the orthogonal complement of U under T is NOT equal to 
    #     the orthogonal complement of the image of U in W.
    try:
        # Orthogonal complement of U in V (U_perp)
        U_perp_basis = (U.T * B_V).nullspace()
        if not U_perp_basis:
            U_perp_mat = zeros(B_V.shape[0], 1)
        else:
            U_perp_mat = Matrix.hstack(*U_perp_basis)
            
        # Image of U_perp under T: T(U_perp)
        T_U_perp = T * U_perp_mat
        
        # Image of U under T: T(U)
        T_U = T * U
        
        # Orthogonal complement of T(U) in W: T(U)_perp
        T_U_perp_basis = (T_U.T * B_W).nullspace()
        if not T_U_perp_basis:
            T_U_perp_mat = zeros(B_W.shape[0], 1)
        else:
            T_U_perp_mat = Matrix.hstack(*T_U_perp_basis)
            
        # Check if T(U_perp) and T(U)_perp span the same subspace
        r1 = T_U_perp.rank()
        r2 = T_U_perp_mat.rank()
        r12 = Matrix.hstack(T_U_perp, T_U_perp_mat).rank()
        
        # They are equal iff their ranks are equal to the rank of their union
        subspaces_equal = (r1 == r2 and r1 == r12)
        neg_q = not subspaces_equal
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces equipped with symmetric bilinear forms B_V and B_W respectively",
    "H_2: U is a subspace of V and T is a linear map from V to W",
    "¬Q: The image of the orthogonal complement of U under T is not equal to the orthogonal complement of the image of U in W"
]

N_HYP = 2
NEG_Q_INDEX = 2
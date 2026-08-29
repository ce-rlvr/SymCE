import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: T is a linear operator on V",
    "H_3: U is a non-zero T-invariant subspace of V",
    "¬Q: lambda is not an eigenvalue of T"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            U = witness.get('U')
            lam = witness.get('lambda', witness.get('lam'))
        elif isinstance(witness, (tuple, list)) and len(witness) >= 3:
            T = witness[-3]
            U = witness[-2]
            lam = witness[-1]
        else:
            T, U, lam = None, None, None
    except Exception:
        T, U, lam = None, None, None

    # H_1: V is a vector space over a field F
    # Implicitly verified if T is a valid square matrix representing an operator on F^n
    try:
        h1 = isinstance(T, Matrix) and T.is_square
    except Exception:
        h1 = False

    # H_2: T is a linear operator on V
    try:
        h2 = isinstance(T, Matrix) and T.is_square
    except Exception:
        h2 = False

    # H_3: U is a non-zero T-invariant subspace of V
    try:
        if isinstance(U, Matrix):
            # If U is provided as a matrix, treat its columns as the basis vectors
            U_list = [U[:, i] for i in range(U.shape[1])]
        else:
            U_list = U
            
        if not isinstance(U_list, (list, tuple)) or len(U_list) == 0:
            h3 = False
        else:
            n = T.shape[0]
            valid_U = all(isinstance(u, Matrix) and u.shape == (n, 1) for u in U_list)
            if not valid_U:
                h3 = False
            else:
                # Form a matrix M whose columns span U
                M = U_list[0]
                for u in U_list[1:]:
                    M = M.row_join(u)
                
                rank_M = M.rank()
                if rank_M == 0:
                    h3 = False  # U must be non-zero
                else:
                    invariant = True
                    for u in U_list:
                        Tu = T * u
                        # Check if Tu is in the span of U
                        M_aug = M.row_join(Tu)
                        if M_aug.rank() > rank_M:
                            invariant = False
                            break
                    h3 = invariant
    except Exception:
        h3 = False

    # ¬Q: lambda is not an eigenvalue of T
    try:
        n = T.shape[0]
        I = eye(n)
        char_mat = T - lam * I
        det_val = sympy.simplify(char_mat.det())
        
        if hasattr(det_val, 'is_zero') and det_val.is_zero is not None:
            neg_q = not det_val.is_zero
        else:
            neg_q = bool(det_val != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
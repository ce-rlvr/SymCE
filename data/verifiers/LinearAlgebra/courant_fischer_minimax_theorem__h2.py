import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (A, k) or (A, k, lambda_k).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                A, k = witness
                lam_provided = False
            elif len(witness) == 3:
                A, k, lam = witness
                lam_provided = True
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: A is an n x n real symmetric matrix
    try:
        h1 = isinstance(A, sp.MatrixBase) and A.is_square and A.is_symmetric()
        if h1:
            for e in A:
                if not e.is_real:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: k is an integer such that 1 <= k <= n
    try:
        n = A.shape[0]
        h2 = isinstance(k, int) and 1 <= k <= n
    except Exception:
        h2 = False

    # ¬Q: lambda_k != max_{dim(V)=k} min_{x \in V, ||x||=1} x^T A x
    try:
        # Compute eigenvalues
        eigs = A.eigenvals()
        eig_list = []
        for val, mult in eigs.items():
            eig_list.extend([val] * mult)
        
        # Sort eigenvalues ascending and descending
        eig_list_asc = sorted(eig_list, key=lambda x: float(sp.re(sp.sympify(x).evalf())))
        eig_list_desc = sorted(eig_list, key=lambda x: float(sp.re(sp.sympify(x).evalf())), reverse=True)
        
        # If lambda_k is not explicitly provided, assume the default ascending order
        if lam_provided:
            lambda_k = lam
        else:
            lambda_k = eig_list_asc[k-1]
            
        # By the Courant-Fischer Minimax Theorem, the RHS evaluates to the k-th largest eigenvalue
        rhs = eig_list_desc[k-1]
        
        # Check if the conclusion fails (i.e., lambda_k != RHS)
        diff = abs(complex(sp.sympify(lambda_k).evalf()) - complex(sp.sympify(rhs).evalf()))
        neg_q = diff > 1e-7
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n real symmetric matrix",
    "H_2: k is an integer such that 1 <= k <= n",
    "¬Q: lambda_k != max_{dim(V)=k} min_{x in V, ||x||=1} x^T A x"
]

N_HYP = 2
NEG_Q_INDEX = 2
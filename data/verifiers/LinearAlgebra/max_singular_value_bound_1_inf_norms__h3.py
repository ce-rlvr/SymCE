import sympy as sp
from sympy import Matrix, I, Abs, sqrt, Max, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    """
    # H_1: A is an m x n complex matrix
    try:
        A = Matrix(witness)
        h1 = True
        for val in A:
            if not val.is_complex:
                h1 = False
                break
    except Exception:
        h1 = False

    # neg_Q: sigma_1(A) > sqrt(||A||_1 ||A||_inf)
    try:
        m, n = A.shape
        if m == 0 or n == 0:
            norm1 = 0
            norm_inf = 0
            max_eig = 0
        else:
            # ||A||_1: maximum absolute column sum norm
            norm1 = max([sum([sp.Abs(A[i, j]) for i in range(m)]) for j in range(n)])
            # ||A||_inf: maximum absolute row sum norm
            norm_inf = max([sum([sp.Abs(A[i, j]) for j in range(n)]) for i in range(m)])
            
            # sigma_1(A)^2 is the maximum eigenvalue of A^H A
            A_H = A.conjugate().transpose()
            M = A_H * A
            eigenvals = M.eigenvals(multiple=True)
            max_eig = max([sp.re(ev) for ev in eigenvals])
            
        max_eig_val = float(sp.N(max_eig))
        bound_val = float(sp.N(norm1 * norm_inf))
        
        # We check if sigma_1(A)^2 > ||A||_1 * ||A||_inf
        # A small relative tolerance is used to avoid false positives from floating point inaccuracies
        neg_q = max_eig_val > bound_val + 1e-9 * max(1.0, bound_val)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a complex matrix",
    "¬Q: sigma_1(A) > sqrt(||A||_1 ||A||_inf)"
]

N_HYP = 1
NEG_Q_INDEX = 1
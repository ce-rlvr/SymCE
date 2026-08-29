import sympy
from sympy import Matrix, eye
import itertools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a list or tuple of sympy.Matrix objects representing 
    a family of linear operators on a finite-dimensional vector space.
    """
    # H_1: V is a non-zero finite-dimensional vector space and F is a family of operators on V
    h1_ok = False
    try:
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            if isinstance(witness[0], Matrix):
                n = witness[0].rows
                if n >= 1:
                    h1_ok = True
                    for M in witness:
                        if not isinstance(M, Matrix) or M.rows != n or M.cols != n:
                            h1_ok = False
                            break
    except Exception:
        h1_ok = False

    # neg_Q: There is no common eigenvector for all operators in F
    neg_q_ok = False
    try:
        if h1_ok:
            n = witness[0].rows
            eigenvalues_list = []
            valid_evs = True
            for M in witness:
                evs = M.eigenvals()
                # Check if SymPy found all eigenvalues (sum of algebraic multiplicities == n)
                # This ensures we are working over an algebraically closed field and didn't miss any.
                if sum(evs.values()) != n:
                    valid_evs = False
                    break
                eigenvalues_list.append(list(evs.keys()))
            
            if valid_evs:
                I = eye(n)
                has_common_eigenvector = False
                # A common eigenvector exists iff there is a combination of eigenvalues
                # such that the intersection of their eigenspaces is non-trivial.
                for combo in itertools.product(*eigenvalues_list):
                    blocks = []
                    for M, lam in zip(witness, combo):
                        blocks.append(M - lam * I)
                    
                    # Stack the matrices (M_i - lambda_i * I) vertically
                    stacked = Matrix.vstack(*blocks)
                    
                    # If the nullspace of the stacked matrix is non-trivial, 
                    # there is a simultaneous eigenvector.
                    if stacked.rank() < n:
                        has_common_eigenvector = True
                        break
                
                neg_q_ok = not has_common_eigenvector
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a non-zero finite-dimensional vector space and F is a family of operators on V",
    "¬Q: There is no common eigenvector for all operators in F"
]

N_HYP = 1
NEG_Q_INDEX = 1
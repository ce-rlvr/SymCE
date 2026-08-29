import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_zero(expr):
    """Helper to check if a sympy expression is mathematically zero."""
    if expr == 0:
        return True
    try:
        return sp.simplify(expr) == 0
    except Exception:
        return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok]
    """
    # H_1: V is a finite-dimensional vector space over a field F
    # We interpret the witness as the matrix representation of the bilinear form B on V.
    try:
        if not hasattr(witness, 'shape') or len(witness.shape) != 2:
            return [False, False]
        if witness.shape[0] != witness.shape[1]:
            return [False, False]
        if not hasattr(witness, 'det'):
            return [False, False]
        h1 = True
    except Exception:
        return [False, False]
        
    # neg_Q: The matrix representation of B is NOT congruent to a block diagonal matrix 
    # with 2x2 blocks of [[0, 1], [-1, 0]].
    # A bilinear form has such a symplectic basis if and only if its matrix is 
    # alternating (skew-symmetric with zero diagonal), non-degenerate, and of even dimension.
    try:
        n = witness.shape[0]
        if n % 2 != 0:
            q = False
        else:
            is_alt = True
            # Check zero diagonal
            for i in range(n):
                if not check_zero(witness[i, i]):
                    is_alt = False
                    break
            # Check skew-symmetry
            if is_alt:
                for i in range(n):
                    for j in range(i + 1, n):
                        if not check_zero(witness[i, j] + witness[j, i]):
                            is_alt = False
                            break
                    if not is_alt:
                        break
            
            if not is_alt:
                q = False
            else:
                # Check non-degeneracy
                det_val = witness.det()
                if check_zero(det_val):
                    q = False
                else:
                    q = True
                    
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "¬Q: B does not have a symplectic basis (matrix is not congruent to the standard symplectic form)"
]

N_HYP = 1
NEG_Q_INDEX = 1
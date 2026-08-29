import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the remaining hypotheses and the negated conclusion for the false conjecture.
    The witness is expected to be a tuple (T, N) or (T, D, N) representing the operator T 
    and its nilpotent part N (and optionally the diagonalizable part D), or a dictionary 
    with keys 'T' and 'N'.
    """
    try:
        # Extract T and N from the witness
        if isinstance(witness, tuple) and len(witness) >= 2:
            T = witness[0]
            N = witness[-1]
        elif isinstance(witness, dict) and 'T' in witness and 'N' in witness:
            T = witness['T']
            N = witness['N']
        else:
            return [False, False]
            
        # H_1: V is a finite-dimensional vector space over an algebraically closed field F
        # We verify this by checking that T and N are square matrices of the same dimension.
        h1 = (isinstance(T, Matrix) and T.is_square and 
              isinstance(N, Matrix) and N.is_square and 
              T.shape == N.shape)
        
        if not h1:
            return [False, False]
            
        # Conclusion: T is diagonalizable if and only if the nilpotent part N is the zero operator.
        # Negation: T is diagonalizable XOR N is the zero operator.
        t_diag = bool(T.is_diagonalizable())
        n_zero = bool(N.is_zero_matrix)
        
        neg_q = (t_diag != n_zero)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over an algebraically closed field F",
    "¬Q: T is diagonalizable if and only if the nilpotent part N is the zero operator (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1
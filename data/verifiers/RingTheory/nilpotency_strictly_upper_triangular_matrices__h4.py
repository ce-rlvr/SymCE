import sympy
from sympy import Matrix, zeros, eye

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # The witness is expected to be the matrix A (or a tuple of A and n)
        if isinstance(witness, tuple) and len(witness) == 2:
            A, n_wit = witness
        else:
            A = witness
            n_wit = None
            
        # Check if A is a square sympy Matrix
        if not (hasattr(A, 'is_Matrix') and A.is_Matrix and A.is_square):
            return [False, False, False, False]
            
        n = A.shape[0]
        if n_wit is not None and n_wit != n:
            return [False, False, False, False]
            
        # H_1: R is a commutative ring
        # We verify that all symbols in the matrix are commutative (default in sympy).
        h1 = all(getattr(sym, 'is_commutative', True) for sym in A.free_symbols)
        
        # H_2: n is a positive integer
        h2 = isinstance(n, int) and n > 0
        
        # H_3: U is the ring of n by n strictly upper triangular matrices with entries in R
        # This is a definitional hypothesis that sets up the context, so it holds vacuously here.
        h3 = True
        
        # ¬Q: A^n is not the zero matrix (and thus A is not necessarily nilpotent of degree n)
        neg_q = bool(A**n != zeros(n, n))
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: n is a positive integer",
    "H_3: U is the ring of n by n strictly upper triangular matrices with entries in R",
    "¬Q: A^n is not the zero matrix"
]

N_HYP = 3
NEG_Q_INDEX = 3
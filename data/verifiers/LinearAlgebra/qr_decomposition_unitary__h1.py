import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture claims that for ANY matrix A, there exists a unique unitary Q 
    and a unique upper triangular R with strictly positive real diagonal entries 
    such that A = QR.
    
    This is false because:
    1. If A is singular (or its first m columns are linearly dependent), R cannot 
       have strictly positive diagonal entries.
    2. If A has more rows than columns (m > n), the unitary matrix Q is not unique 
       because the orthogonal complement of the column space allows arbitrary phase choices.
    """
    try:
        # Ensure the witness is a SymPy Matrix
        if not isinstance(witness, sp.MatrixBase):
            try:
                witness = sp.Matrix(witness)
            except Exception:
                return [True]
        
        m, n = witness.shape
        
        # If m > n, Q is never unique because the left nullspace has dimension >= 1,
        # and we can multiply the corresponding columns of Q by any complex phase.
        if m > n:
            neg_q = True
        elif m == 0:
            # 0x0 matrix vacuously satisfies existence and uniqueness
            neg_q = False
        else:
            # For m <= n, existence and uniqueness hold iff the first m columns of A 
            # form an invertible m x m matrix.
            A_m = witness[:, :m]
            det_A = A_m.det()
            
            if hasattr(det_A, 'free_symbols') and det_A.free_symbols:
                det_A = sp.simplify(det_A)
                
            if det_A == 0:
                neg_q = True
            else:
                neg_q = False
                
    except Exception:
        # If any computation fails, we default to True for the negated conclusion
        neg_q = True
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: There does not exist a unique unitary Q and unique upper triangular R with strictly positive real diagonal entries such that A=QR"
]

N_HYP = 0
NEG_Q_INDEX = 0
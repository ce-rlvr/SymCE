import sympy
from sympy import Matrix, eye, zeros

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a single matrix A, or a tuple (A, J) where J is a proposed matrix.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A_in, J_in = witness
        else:
            A_in = witness
            J_in = None
            
        if not isinstance(A_in, Matrix):
            A = Matrix(A_in)
        else:
            A = A_in
            
        if J_in is None:
            J = A.jordan_form()[1]
        else:
            if not isinstance(J_in, Matrix):
                J = Matrix(J_in)
            else:
                J = J_in
    except Exception:
        return [False, False]

    # H_1: Let A be an n \times n complex matrix.
    try:
        h1 = A.is_square
    except Exception:
        h1 = False

    # neg_Q: The total number of ones on the superdiagonal of J is NOT exactly n - sum(dim(ker(A - lambda I)))
    try:
        n = A.shape[0]
        
        # Count ones on the superdiagonal of J
        ones_on_superdiagonal = 0
        limit = min(J.shape[0], J.shape[1])
        for i in range(limit - 1):
            if J[i, i+1] == 1:
                ones_on_superdiagonal += 1
                
        # Compute sum of geometric multiplicities (dim(ker(A - lambda I)))
        sum_dim_ker = 0
        for lam, alg_mult, basis in A.eigenvects():
            sum_dim_ker += len(basis)
            
        expected_ones = n - sum_dim_ker
        
        # The conclusion fails if the actual number of ones does not match the expected formula
        neg_q = (ones_on_superdiagonal != expected_ones)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "¬Q: The total number of ones on the superdiagonal of J is not exactly n - sum(dim(ker(A - lambda I)))"
]

N_HYP = 1
NEG_Q_INDEX = 1
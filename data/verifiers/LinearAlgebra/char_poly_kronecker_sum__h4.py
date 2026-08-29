import sympy as sp

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def kronecker_product(A, B):
    """Computes the Kronecker product of two SymPy matrices."""
    m, n = A.shape
    p, q = B.shape
    return sp.Matrix(m * p, n * q, lambda i, j: A[i // p, j // q] * B[i % p, j % q])

def conditions(witness):
    try:
        A, B = witness
    except Exception:
        return [False, False, False]
        
    try:
        H1 = isinstance(A, sp.MatrixBase) and A.is_square
    except Exception:
        H1 = False
        
    try:
        H2 = isinstance(B, sp.MatrixBase) and B.is_square
    except Exception:
        H2 = False
        
    try:
        if not (H1 and H2):
            neg_Q = False
        else:
            n = A.shape[0]
            m = B.shape[0]
            
            I_m = sp.eye(m)
            I_n = sp.eye(n)
            
            # Kronecker sum: A (x) I_m + I_n (x) B
            K = kronecker_product(A, I_m) + kronecker_product(I_n, B)
            
            x = sp.Symbol('x')
            cp1 = K.charpoly(x).as_expr()
            
            A_eigenvals = list(A.eigenvals(multiple=True))
            B_eigenvals = list(B.eigenvals(multiple=True))
            
            # Ensure we have all eigenvalues (algebraic multiplicity sums to dimension)
            if len(A_eigenvals) != n or len(B_eigenvals) != m:
                neg_Q = False
            else:
                cp2 = sp.sympify(1)
                for l in A_eigenvals:
                    for mu in B_eigenvals:
                        cp2 *= (x - (l + mu))
                        
                diff = sp.simplify(sp.expand(cp1) - sp.expand(cp2))
                neg_Q = bool(diff != 0)
    except Exception:
        neg_Q = False
        
    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "H_2: B is a square matrix",
    "¬Q: The characteristic polynomial of A (x) I_m + I_n (x) B is not the product of (x - (lambda_i + mu_j))"
]

N_HYP = 2
NEG_Q_INDEX = 2
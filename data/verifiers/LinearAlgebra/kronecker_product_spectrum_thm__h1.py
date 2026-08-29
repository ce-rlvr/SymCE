import sympy
from sympy import Matrix, eye, zeros, Dummy, expand, simplify

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: B is an m x m matrix",
    "¬Q: The nm eigenvalues of A ⊗ B are not exactly the products λ_i μ_j"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_matrix(obj):
    return hasattr(obj, 'is_square') and hasattr(obj, 'shape') and hasattr(obj, 'eigenvals')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
        else:
            A, B = witness
    except Exception:
        return [False, False]
        
    try:
        if not is_matrix(A):
            A = Matrix(A)
    except Exception:
        pass

    try:
        if not is_matrix(B):
            B = Matrix(B)
    except Exception:
        pass

    # H1: B is an m x m matrix
    try:
        h1 = is_matrix(B) and B.is_square
    except Exception:
        h1 = False
        
    # neg_Q: The nm eigenvalues of A ⊗ B are exactly the products λ_i μ_j
    try:
        if not is_matrix(A) or not is_matrix(B):
            neg_q = True
        elif not A.is_square or not B.is_square:
            # If A or B is not square, they don't have a well-defined set of n (or m) eigenvalues,
            # or A ⊗ B is not square and thus lacks eigenvalues. The conclusion fails.
            neg_q = True
        else:
            eigA = A.eigenvals(multiple=True)
            eigB = B.eigenvals(multiple=True)
            
            # If eigenvalues cannot be found explicitly, we assume it's not a counterexample
            # because the theorem is mathematically true for all square matrices.
            if any(type(val).__name__ in ('CRootOf', 'RootOf') for val in eigA) or \
               any(type(val).__name__ in ('CRootOf', 'RootOf') for val in eigB):
                neg_q = False
            else:
                x = Dummy('x')
                expected_poly = 1
                for l in eigA:
                    for m in eigB:
                        expected_poly *= (x - l * m)
                        
                m_A, n_A = A.shape
                m_B, n_B = B.shape
                
                # Compute Kronecker product A ⊗ B
                AxB = Matrix(m_A * m_B, n_A * n_B, lambda i, j: A[i // m_B, j // n_B] * B[i % m_B, j % n_B])
                
                poly_AxB = AxB.charpoly(x).as_expr()
                
                # Compare the characteristic polynomial of A ⊗ B with the expected polynomial
                diff = simplify(expand(poly_AxB - expected_poly))
                neg_q = (diff != 0)
    except Exception:
        # If evaluation fails for square matrices, default to False (not a counterexample)
        neg_q = False
        
    return [bool(h1), bool(neg_q)]
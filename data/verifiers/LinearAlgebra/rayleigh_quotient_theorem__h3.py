import sympy
from sympy import Matrix, simplify, expand, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (A, x) where A is a matrix and x is a vector.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        A, x = witness
    except Exception:
        return [False, False, False]

    # H_1: A is an n x n matrix with real entries
    try:
        h1 = isinstance(A, Matrix) and A.is_square and A.shape[0] >= 1 and all(e.is_real for e in A)
    except Exception:
        h1 = False

    # H_2: A is a symmetric matrix
    try:
        h2 = bool(A.is_symmetric())
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails
    # Conclusion: (x^T A x) / (x^T x) <= max_eig, with equality iff x is an eigenvector for max_eig.
    try:
        if not (isinstance(x, Matrix) and x.shape == (A.shape[0], 1) and all(e.is_real for e in x)):
            neg_q = False
        else:
            num = (x.T * A * x)[0, 0]
            den = (x.T * x)[0, 0]
            
            if den == 0:
                # The Rayleigh quotient is undefined, so the conclusion statement is false.
                q = False
            else:
                R = simplify(num / den)
                eigenvals = A.eigenvals()
                
                if not eigenvals:
                    q = False
                else:
                    # Find the maximum eigenvalue (using real part for comparison if complex)
                    max_eig = max(eigenvals.keys(), key=lambda val: float(sympy.re(val.evalf())))
                    
                    R_val = float(sympy.re(R.evalf()))
                    max_eig_val = float(sympy.re(max_eig.evalf()))
                    
                    # Check if R <= max_eig
                    if R_val > max_eig_val + 1e-7:
                        q = False
                    else:
                        # Check the equality condition
                        is_equal = simplify(expand(R - max_eig)) == 0
                        
                        # Check if x is an eigenvector associated with max_eig
                        diff = A * x - max_eig * x
                        is_eigenvec = all(simplify(expand(e)) == 0 for e in diff) and not all(simplify(expand(e)) == 0 for e in x)
                        
                        if is_equal != is_eigenvec:
                            q = False
                        else:
                            q = True
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with real entries",
    "H_2: A is a symmetric matrix",
    "¬Q: The Rayleigh quotient is undefined, strictly greater than the maximum eigenvalue, or the equality condition fails"
]

N_HYP = 2
NEG_Q_INDEX = 2
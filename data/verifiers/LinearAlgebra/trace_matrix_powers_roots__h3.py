import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is an algebraically closed field",
    "H_2: A is an n \\times n matrix over F",
    "¬Q: For some positive integer k, the trace of A^k is not equal to the sum of lambda_i^k"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    
    The witness is expected to be a SymPy Matrix.
    """
    # H_1: F is an algebraically closed field
    # In SymPy, matrices over symbolic or complex domains implicitly satisfy this.
    # We verify the witness is a valid SymPy matrix.
    try:
        h1 = isinstance(witness, sympy.MatrixBase)
    except Exception:
        h1 = False

    # H_2: A is an n \times n matrix over F
    try:
        h2 = h1 and witness.is_square
    except Exception:
        h2 = False

    # ¬Q: For some positive integer k, the trace of A^k is not equal to \sum_{i=1}^n \lambda_i^k
    neg_q = False
    if h2:
        try:
            eigenvals = witness.eigenvals()
            n = witness.shape[0]
            
            # Proceed only if SymPy successfully found all n eigenvalues (counting algebraic multiplicity)
            if sum(eigenvals.values()) == n:
                # Check for positive integers k (we test 1 through 10)
                for k in range(1, 11):
                    tr = (witness**k).trace()
                    sum_lam = sum((lam**k) * mult for lam, mult in eigenvals.items())
                    
                    # Verify if trace(A^k) != sum(lambda_i^k)
                    diff = sympy.cancel(sympy.simplify(tr - sum_lam))
                    if diff != 0:
                        neg_q = True
                        break
        except Exception:
            pass

    return [h1, h2, neg_q]
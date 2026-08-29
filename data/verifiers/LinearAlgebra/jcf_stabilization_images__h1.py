import sympy
from sympy import eye, zeros

# Top-level setup for standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: lambda is an eigenvalue of A",
    "H_2: m is the index of lambda",
    "not Q: The sequence of dimensions does not strictly decrease for 0 <= k <= m, or does not remain constant for k >= m"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness, checks whether it is a valid counterexample.
    The witness can be a dictionary (representing an infinite-dimensional operator),
    a custom object, or a tuple (A, lambda_val, m).
    """
    # 1. Try dictionary interface (useful for infinite-dimensional counterexamples)
    if isinstance(witness, dict):
        try:
            h1 = witness.get('is_eigenvalue', False)
            m = witness.get('index', -1)
            h2 = (m >= 0)
            dims = witness.get('dims', [])
            
            strictly_decreases = True
            for k in range(m):
                if dims[k] <= dims[k+1]:
                    strictly_decreases = False
                    break
                    
            if len(dims) > m + 1:
                remains_constant = (dims[m] == dims[m+1])
            else:
                remains_constant = False
                
            neg_q = not (strictly_decreases and remains_constant)
            return [bool(h1), bool(h2), bool(neg_q)]
        except Exception:
            pass

    # 2. Try object with attributes
    if not isinstance(witness, (tuple, list)):
        try:
            witness = (witness.A, witness.lambda_val, witness.m)
        except Exception:
            pass

    # 3. Try tuple (A, lambda_val, m)
    try:
        A, lambda_val, m = witness
    except Exception:
        return [False, False, False]

    # H1: lambda_val is an eigenvalue of A
    try:
        if hasattr(A, 'shape'):
            I = eye(A.shape[0])
            N = A - lambda_val * I
            h1 = len(N.nullspace()) > 0
        else:
            h1 = A.is_eigenvalue(lambda_val)
    except Exception:
        h1 = False

    # H2: m is the index of lambda_val
    try:
        if hasattr(A, 'shape'):
            actual_m = 0
            while True:
                if (N**actual_m).rank() == (N**(actual_m+1)).rank():
                    break
                actual_m += 1
            h2 = (m == actual_m)
        else:
            h2 = (A.index(lambda_val) == m)
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails
    try:
        if hasattr(A, 'shape'):
            dims = [(N**k).rank() for k in range(m + 2)]
        else:
            dims = [A.image_dim(lambda_val, k) for k in range(m + 2)]
            
        strictly_decreases = True
        for k in range(m):
            if dims[k] <= dims[k+1]:
                strictly_decreases = False
                break
        remains_constant = (dims[m] == dims[m+1])
        
        neg_q = not (strictly_decreases and remains_constant)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]
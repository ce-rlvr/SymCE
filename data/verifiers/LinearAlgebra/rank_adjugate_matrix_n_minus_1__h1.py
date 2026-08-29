import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n >= 2",
    "H_2: The rank of A is exactly n - 1",
    "not Q: The rank of the adjugate matrix adj(A) is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    n = None
    A = None
    
    # Unpack witness if it's a tuple (e.g., (n, A) or (A, n))
    if isinstance(witness, tuple):
        for item in witness:
            if isinstance(item, int):
                n = item
            else:
                A = item
    else:
        A = witness
        
    # Convert to sympy Matrix if it's a list of lists or similar
    try:
        if not hasattr(A, 'adjugate'):
            A = sympy.Matrix(A)
    except Exception:
        pass

    # Infer n if not explicitly provided
    if n is None:
        try:
            if hasattr(A, 'shape') and len(A.shape) >= 2:
                # Check if row count or column count satisfies the rank condition
                if A.shape[0] >= 2 and A.rank() == A.shape[0] - 1:
                    n = A.shape[0]
                elif A.shape[1] >= 2 and A.rank() == A.shape[1] - 1:
                    n = A.shape[1]
                else:
                    n = A.shape[0]  # default fallback
            else:
                n = 0
        except Exception:
            n = 0

    # Evaluate Hypothesis 1: n >= 2
    try:
        h1 = bool(n >= 2)
    except Exception:
        h1 = False
        
    # Evaluate Hypothesis 2: The rank of A is exactly n - 1
    try:
        h2 = bool(A.rank() == n - 1)
    except Exception:
        h2 = False
        
    # Evaluate Negated Conclusion: The rank of adj(A) is NOT exactly 1
    try:
        adj_A = A.adjugate()
        neg_q = bool(adj_A.rank() != 1)
    except Exception:
        # If adjugate cannot be computed (e.g., A is not a square matrix),
        # the conclusion "rank of adj(A) is exactly 1" is false, so its negation is true.
        neg_q = True
        
    return [h1, h2, neg_q]
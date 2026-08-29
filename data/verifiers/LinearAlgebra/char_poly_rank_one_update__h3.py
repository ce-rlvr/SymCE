import sympy as sp
from sympy import eye, zeros, Rational, Integer, Symbol

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Given a witness (A, u, v), checks if it satisfies the hypotheses
    and falsifies the conclusion of the conjecture.
    """
    try:
        A, u, v = witness
    except Exception:
        return [False, False, False]
        
    # H_1: A is an n x n matrix over a field F
    try:
        h1 = isinstance(A, sp.MatrixBase) and A.is_square
        n = A.shape[0]
    except Exception:
        h1 = False
        n = 0
        
    # H_2: u and v are n x 1 column vectors over F
    try:
        h2 = isinstance(u, sp.MatrixBase) and u.shape == (n, 1) and \
             isinstance(v, sp.MatrixBase) and v.shape == (n, 1)
    except Exception:
        h2 = False
        
    # ¬Q: The characteristic polynomial of A + uv^T is NOT p_A(t) - v^T adj(tI - A) u
    try:
        t = sp.Symbol('t')
        
        # Compute characteristic polynomials (defined as det(tI - M) in SymPy)
        pA = A.charpoly(t).as_expr()
        pA_uv = (A + u * v.T).charpoly(t).as_expr()
        
        if n == 0:
            update = 0
        else:
            # Compute adj(tI - A)
            adj = (t * sp.eye(n) - A).adjugate()
            # Compute v^T adj(tI - A) u and extract the scalar
            update = (v.T * adj * u)[0]
            
        # Check if the mathematical identity holds
        diff = sp.simplify(pA_uv - (pA - update))
        neg_Q = not (diff == 0)
    except Exception:
        # If evaluation fails (e.g., type mismatch or undefined operations), 
        # we consider the conclusion to have failed.
        neg_Q = True
        
    return [h1, h2, neg_Q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field F",
    "H_2: u and v are n x 1 column vectors over F",
    "¬Q: The characteristic polynomial of A + uv^T is not p_A(t) - v^T adj(tI - A) u"
]

N_HYP = 2
NEG_Q_INDEX = 2
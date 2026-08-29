import sympy as sp

# Top-level setup for standard linear algebra objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (A, B) or a dictionary containing 
    the transformation matrices A (for T) and B (for S).
    """
    # Extract matrices A and B from the witness
    try:
        if isinstance(witness, dict):
            A = sp.Matrix(witness.get('T', witness.get('A')))
            B = sp.Matrix(witness.get('S', witness.get('B')))
        else:
            A = sp.Matrix(witness[0])
            B = sp.Matrix(witness[1])
    except Exception:
        return [False, False, False]
        
    # H_1: T: V -> W and S: W -> V are linear transformations
    # If T is represented by an m x n matrix A, then S must be an n x m matrix B.
    try:
        m, n = A.shape
        h1 = (B.shape == (n, m))
    except Exception:
        h1 = False
        
    # H_2: S \circ T = I_V
    # The composition S \circ T is represented by the matrix product B * A.
    try:
        I_v = sp.eye(n)
        BA = B * A
        if BA == I_v:
            h2 = True
        else:
            diff = sp.simplify(BA - I_v)
            h2 = bool(diff == sp.zeros(n, n))
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion FAILS at the witness.
    # Conclusion: T* \circ S* = I_{V*}
    # T* is represented by A^T and S* is represented by B^T.
    # The composition T* \circ S* (S* followed by T*) is represented by A^T * B^T.
    # We check if A^T * B^T != I_{V*}. (This can happen for matrices over non-commutative rings).
    try:
        I_v_star = sp.eye(n)
        ATBT = A.T * B.T
        if ATBT == I_v_star:
            neg_q = False
        else:
            diff = sp.simplify(ATBT - I_v_star)
            neg_q = not bool(diff == sp.zeros(n, n))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T: V -> W and S: W -> V are linear transformations",
    "H_2: S \\circ T = I_V",
    "¬Q: T* \\circ S* \\neq I_{V*}"
]

N_HYP = 2
NEG_Q_INDEX = 2
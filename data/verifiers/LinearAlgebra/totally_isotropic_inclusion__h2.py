import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple (B, W) where:
      - B is an n x n sympy Matrix representing the bilinear form on V.
      - W is an n x k sympy Matrix whose columns span the subspace W.
    """
    try:
        B, W = witness
        B = sympy.Matrix(B)
        W = sympy.Matrix(W)
    except Exception:
        return [False, False, False]
    
    def is_zero_matrix(M):
        try:
            return all(sympy.simplify(M[i, j]) == 0 for i in range(M.shape[0]) for j in range(M.shape[1]))
        except Exception:
            return False

    # H_1: V is a vector space over a field F
    try:
        h1 = bool(B.is_square and B.shape[0] == W.shape[0])
    except Exception:
        h1 = False

    # H_2: W is a totally isotropic subspace of V with respect to B
    # A subspace is totally isotropic if B(x, x) = 0 for all x in W.
    # For M = W^T * B * W, this means x^T * M * x = 0 for all x,
    # which is equivalent to M having a zero diagonal and M + M^T = 0.
    try:
        if not h1:
            h2 = False
        else:
            M = W.T * B * W
            k = M.shape[0]
            diag_zero = all(sympy.simplify(M[i, i]) == 0 for i in range(k))
            skew_sym = is_zero_matrix(M + M.T)
            h2 = bool(diag_zero and skew_sym)
    except Exception:
        h2 = False

    # ¬Q: W is not a subspace of its orthogonal complement W^\perp
    # W is a subspace of W^\perp iff B(x, y) = 0 for all x, y in W.
    # This is equivalent to M = W^T * B * W being the zero matrix.
    # The negation is that M is NOT the zero matrix.
    try:
        if not h1:
            neg_q = False
        else:
            M = W.T * B * W
            neg_q = not is_zero_matrix(M)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: W is a totally isotropic subspace of V with respect to B",
    "¬Q: W is not a subspace of its orthogonal complement W^\\perp"
]

N_HYP = 2
NEG_Q_INDEX = 2
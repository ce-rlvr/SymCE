import sympy
from sympy import Matrix, expand, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Given a witness, checks whether it is a valid counterexample to the false conjecture:
    "S is linearly independent if and only if det(G) != 0"
    
    The witness can be a tuple:
      - (S, G) where S is a list of vectors and G is the Gram matrix (assumes standard symmetric bilinear form u.T * v)
      - (S, G, M) where M is the matrix defining the inner product <u, v> = u.T * M * v
      - (S, G, inner_product_func) where inner_product_func is a callable
    """
    try:
        if len(witness) == 3:
            S_raw, G_raw, third = witness
        elif len(witness) == 2:
            S_raw, G_raw = witness
            third = None
        else:
            return [False, False, False]
            
        S = [Matrix(v) for v in S_raw]
        G = Matrix(G_raw)
        
        if third is not None:
            if callable(third):
                inner_product = third
                h1 = isinstance(S, list) and len(S) > 0
            else:
                M = Matrix(third)
                inner_product = lambda u, v: (u.T * M * v)[0, 0]
                h1 = isinstance(S, list) and len(S) > 0 and M.is_square and M == M.T and M.det() != 0
        else:
            inner_product = lambda u, v: (u.T * v)[0, 0]
            h1 = isinstance(S, list) and len(S) > 0
            
        if h1:
            dim = S[0].shape[0]
            h1 = all(v.shape == (dim, 1) for v in S)
    except Exception:
        return [False, False, False]

    try:
        n = len(S)
        h2 = G.shape == (n, n)
        if h2:
            for i in range(n):
                for j in range(n):
                    diff = G[i, j] - inner_product(S[i], S[j])
                    if diff != 0:
                        if expand(diff) != 0:
                            h2 = False
                            break
    except Exception:
        h2 = False

    try:
        A = sympy.Matrix.hstack(*S)
        is_indep = (A.rank() == n)
        
        det_G = G.det()
        det_G_nonzero = (det_G != 0)
        if det_G != 0:
            if expand(det_G) == 0:
                det_G_nonzero = False
                
        q = (is_indep == det_G_nonzero)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is an inner product space",
    "H_2: G is the n x n matrix whose (i, j)-th entry is <v_i, v_j>",
    "¬Q: S is linearly independent if and only if det(G) != 0 fails"
]

N_HYP = 2
NEG_Q_INDEX = 2
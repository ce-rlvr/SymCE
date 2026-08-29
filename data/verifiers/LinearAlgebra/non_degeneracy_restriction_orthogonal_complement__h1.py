import sympy
from sympy import Matrix, eye, zeros, S

# Top-level setup for Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (B, W) where:
      - B is a SymPy Matrix representing the symmetric bilinear form on V.
      - W is a SymPy Matrix whose columns form a basis for the subspace W, 
        or a list of SymPy column vectors.
    Alternatively, the witness can be a custom object with methods H1(), H2(), and neg_Q().
    """
    # Try to unpack as a tuple of matrices
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                _, B, W = witness
            elif len(witness) == 2:
                B, W = witness
            else:
                raise ValueError
                
            if isinstance(W, list):
                if not W:
                    W_mat = Matrix(B.rows, 0, [])
                else:
                    W_mat = W[0].row_join(*W[1:]) if len(W) > 1 else W[0]
            else:
                W_mat = W
                
            # H1: B is a non-degenerate symmetric bilinear form on V
            h1 = B.is_symmetric() and (B.det() != 0)
            
            # H2: W is a subspace of V such that B|W is non-degenerate
            if W_mat.cols == 0:
                h2 = True
            else:
                B_W = W_mat.T * B * W_mat
                h2 = (B_W.det() != 0)
                
            # neg_Q: The restriction of B to W^\perp \times W^\perp is degenerate
            if W_mat.cols == 0:
                neg_q = (B.det() == 0)
            else:
                W_perp = (W_mat.T * B).nullspace()
                if not W_perp:
                    neg_q = False
                else:
                    W_perp_mat = W_perp[0].row_join(*W_perp[1:]) if len(W_perp) > 1 else W_perp[0]
                    B_W_perp = W_perp_mat.T * B * W_perp_mat
                    neg_q = (B_W_perp.det() == 0)
                    
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # Fallback for custom objects representing infinite-dimensional spaces
    try:
        h1 = witness.H1()
    except Exception:
        h1 = False
    try:
        h2 = witness.H2()
    except Exception:
        h2 = False
    try:
        neg_q = witness.neg_Q()
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: B is a non-degenerate symmetric bilinear form on V",
    "H_2: W is a subspace of V such that the restriction of B to W \\times W is non-degenerate",
    "¬Q: The restriction of B to W^\\perp \\times W^\\perp is degenerate"
]

N_HYP = 2
NEG_Q_INDEX = 2
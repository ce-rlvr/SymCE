import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Witness is expected to be a tuple (B, W) or (V, W, B) or a dict with keys 'B' and 'W',
    where B is the bilinear form matrix and W is a list of basis vectors for the subspace.
    """
    try:
        if isinstance(witness, dict):
            B = witness.get('B')
            W = witness.get('W')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                B, W = witness
            elif len(witness) == 3:
                _, W, B = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        if hasattr(W, 'shape') and len(W.shape) == 2:
            W_vecs = [W[:, i] for i in range(W.shape[1])]
            valid_W = True
        elif isinstance(W, list):
            W_vecs = W
            valid_W = True
        else:
            W_vecs = []
            valid_W = False
    except Exception:
        W_vecs = []
        valid_W = False

    # H1: V is a vector space over the real numbers
    try:
        n = B.shape[0]
        h1 = hasattr(B, 'shape') and len(B.shape) == 2 and (B.shape[0] == B.shape[1]) and n >= 1
    except Exception:
        h1 = False

    # H2: W is a subspace of V
    try:
        if not valid_W:
            h2 = False
        else:
            h2 = True
            for w in W_vecs:
                if not hasattr(w, 'shape') or w.shape != (n, 1):
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: The restriction of B to W x W is NOT a positive definite bilinear form on W
    try:
        if not W_vecs:
            basis = []
        else:
            C_span = Matrix.hstack(*W_vecs)
            _, indep = C_span.rref()
            basis = [C_span[:, i] for i in indep]
        
        if not basis:
            # 0-dimensional subspace: restriction is vacuously positive definite
            neg_q = False
        else:
            C = Matrix.hstack(*basis)
            M = C.T * B * C
            
            # A bilinear form is positive definite if its matrix is symmetric and positive definite
            is_sym = M.is_symmetric()
            is_pd = True
            if is_sym:
                # Sylvester's criterion for positive definiteness
                for i in range(1, M.shape[0] + 1):
                    det_val = M[:i, :i].det()
                    try:
                        if float(det_val) <= 0:
                            is_pd = False
                            break
                    except TypeError:
                        if det_val <= 0:
                            is_pd = False
                            break
            else:
                is_pd = False
                
            neg_q = not is_pd
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over the real numbers",
    "H_2: W is a subspace of V",
    "¬Q: The restriction of B to W \\times W is not a positive definite bilinear form on W"
]

N_HYP = 2
NEG_Q_INDEX = 2
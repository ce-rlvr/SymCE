import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    M = None
    
    # Handle tuple witness (e.g., (Matrix, Field))
    if isinstance(witness, tuple) and len(witness) > 0:
        M_cand = witness[0]
    else:
        M_cand = witness

    # Extract matrix representation
    if isinstance(M_cand, sympy.MatrixBase):
        M = M_cand
    elif isinstance(M_cand, list) and all(isinstance(row, list) for row in M_cand):
        try:
            M = sympy.Matrix(M_cand)
        except Exception:
            pass
    elif isinstance(M_cand, sympy.Expr):
        try:
            vars = list(M_cand.free_symbols)
            if len(vars) >= 2:
                H = sympy.hessian(M_cand, vars)
                if not H.free_symbols:
                    M = H / 2
        except Exception:
            pass

    try:
        # H_1: V is a vector space over K of dimension n >= 2
        h1 = M is not None and M.is_square and M.shape[0] >= 2
    except Exception:
        h1 = False

    try:
        # H_2: q: V \to K is a quadratic form (represented by a symmetric matrix)
        h2 = h1 and M.is_symmetric()
    except Exception:
        h2 = False

    try:
        # ¬Q: There is NO non-zero vector v such that q(v) = 0.
        # A sufficient condition for a real/rational quadratic form to be anisotropic
        # is that its matrix is positive definite or negative definite.
        neg_q = False
        if h2:
            if M.is_positive_definite == True or M.is_negative_definite == True:
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a vector space over K of dimension n >= 2",
    "H_2: q: V -> K is a quadratic form",
    "¬Q: q is anisotropic (there is no non-zero v such that q(v) = 0)"
]

N_HYP = 2
NEG_Q_INDEX = 2
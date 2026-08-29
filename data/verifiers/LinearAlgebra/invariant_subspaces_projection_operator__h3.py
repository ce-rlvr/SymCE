import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    Hypotheses:
      - V is a vector space.
      - P is a linear operator on V such that P^2 = P.
    Conclusion:
      - The subspace W decomposes as the direct sum W = (W \cap im(P)) \oplus (W \cap ker(P)).
      
    The witness should be a tuple (P, W) where:
      - P is a square sympy Matrix representing the projection operator.
      - W is a sympy Matrix whose columns span the subspace W.
    """
    try:
        P, W = witness
    except Exception:
        return [False, False, False]
    
    # H_1: V is a vector space (and W is a subspace of V)
    try:
        P = Matrix(P)
        if isinstance(W, list) and len(W) > 0 and hasattr(W[0], 'rows'):
            W = Matrix.hstack(*[Matrix(w) for w in W])
        else:
            W = Matrix(W)
        h1 = P.is_square and P.rows == W.rows
    except Exception:
        h1 = False

    # H_2: P is a linear operator on V such that P^2 = P
    try:
        if h1:
            if P * P == P:
                h2 = True
            else:
                h2 = sympy.simplify(P * P - P).is_zero_matrix
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: W does NOT decompose as (W \cap im(P)) \oplus (W \cap ker(P))
    # This happens if dim(W) != dim(W \cap im(P)) + dim(W \cap ker(P))
    try:
        if not h1:
            neg_q = False
        else:
            dim_W = W.rank()
            
            # Intersection with im(P)
            im_P = P
            dim_im_P = im_P.rank()
            dim_W_plus_im_P = Matrix.hstack(W, im_P).rank()
            dim_W_cap_im_P = dim_W + dim_im_P - dim_W_plus_im_P
            
            # Intersection with ker(P)
            null_basis = P.nullspace()
            if null_basis:
                ker_P = Matrix.hstack(*null_basis)
            else:
                ker_P = zeros(P.rows, 1)
            dim_ker_P = ker_P.rank()
            dim_W_plus_ker_P = Matrix.hstack(W, ker_P).rank()
            dim_W_cap_ker_P = dim_W + dim_ker_P - dim_W_plus_ker_P
            
            neg_q = bool(dim_W != dim_W_cap_im_P + dim_W_cap_ker_P)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: P is a linear operator on V such that P^2 = P",
    "¬Q: W does not decompose as (W ∩ im(P)) ⊕ (W ∩ ker(P))"
]

N_HYP = 2
NEG_Q_INDEX = 2
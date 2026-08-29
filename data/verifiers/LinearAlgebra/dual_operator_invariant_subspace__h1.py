import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - T is a linear operator on V
      - W is a subspace of V that is invariant under T
    Conclusion:
      - The annihilator W^0 is invariant under the dual operator T^*
    """
    try:
        T, W = witness
    except Exception:
        return [False, False, False]
        
    # H_1: T is a linear operator on V
    try:
        h1 = isinstance(T, Matrix) and T.is_square
        n = T.shape[0]
    except Exception:
        h1 = False
        n = 0

    # H_2: W is a subspace of V invariant under T
    try:
        if isinstance(W, list):
            if len(W) == 0:
                W_mat = zeros(n, 1)
            else:
                W_mat = Matrix.hstack(*W)
        else:
            W_mat = W
            
        if not isinstance(W_mat, Matrix) or W_mat.shape[0] != n:
            h2 = False
        else:
            h2 = True
            rank_W = W_mat.rank()
            for i in range(W_mat.shape[1]):
                w = W_mat[:, i]
                Tw = T * w
                aug = Matrix.hstack(W_mat, Tw)
                if aug.rank() > rank_W:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: W^0 is not invariant under T^*
    try:
        # W^0 is the nullspace of W_mat.T
        W0_basis = W_mat.T.nullspace()
        if len(W0_basis) == 0:
            W0_mat = zeros(n, 1)
        else:
            W0_mat = Matrix.hstack(*W0_basis)
            
        rank_W0 = W0_mat.rank()
        
        q_holds = True
        # T^* acts on W^0 via left multiplication by T, which is right multiplication by T.T on column vectors
        for u in W0_basis:
            T_star_u = T.T * u
            aug = Matrix.hstack(W0_mat, T_star_u)
            if aug.rank() > rank_W0:
                q_holds = False
                break
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: W is a subspace of V invariant under T",
    "¬Q: W^0 is not invariant under T^*"
]

N_HYP = 2
NEG_Q_INDEX = 2
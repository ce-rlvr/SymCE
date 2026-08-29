import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture.
    Witness is expected to be a tuple (U, W_basis), where:
      - U is an n x n sympy.Matrix representing a linear operator on V = C^n.
      - W_basis is a list of n x 1 sympy.Matrix objects representing a spanning set for W.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        
        U, W_basis = witness
        
        # H_1: V is a finite-dimensional inner product space.
        # We verify that U is a square matrix and W_basis contains vectors of the correct dimension.
        if not isinstance(U, sp.Matrix) or U.rows != U.cols:
            h1 = False
        else:
            n = U.rows
            if not isinstance(W_basis, list):
                h1 = False
            else:
                h1 = True
                for w in W_basis:
                    if not isinstance(w, sp.Matrix) or w.rows != n or w.cols != 1:
                        h1 = False
                        break
    except Exception:
        h1 = False

    try:
        # H_2: W is a U-invariant subspace of V.
        if not h1:
            h2 = False
        elif len(W_basis) == 0:
            h2 = True
        else:
            M = sp.Matrix.hstack(*W_basis)
            rank_M = M.rank()
            h2 = True
            for w in W_basis:
                Uw = U * w
                M_aug = sp.Matrix.hstack(M, Uw)
                if M_aug.rank() > rank_M:
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        # ¬Q: U|_W is not a unitary operator on W.
        # U|_W is unitary iff it preserves the inner product on W.
        # For any x, y in W, <Ux, Uy> = <x, y>.
        # Let M be the matrix whose columns span W. Any x in W is M*a for some vector a.
        # <U*M*a, U*M*b> = b^H * M^H * U^H * U * M * a.
        # <M*a, M*b> = b^H * M^H * M * a.
        # Thus, U|_W is unitary iff M^H * U^H * U * M == M^H * M.
        if not h1:
            neg_q = False
        elif len(W_basis) == 0:
            # The restriction to the trivial subspace is trivially unitary.
            neg_q = False
        else:
            M = sp.Matrix.hstack(*W_basis)
            LHS = M.H * U.H * U * M
            RHS = M.H * M
            diff = sp.expand(LHS - RHS)
            
            is_unitary = True
            for i in range(diff.rows):
                for j in range(diff.cols):
                    val = sp.simplify(diff[i, j])
                    if val != 0 and val.is_zero is not True:
                        is_unitary = False
                        break
                if not is_unitary:
                    break
            neg_q = not is_unitary
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "H_2: W is a U-invariant subspace of V",
    "¬Q: U|_W is not a unitary operator on W"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a counterexample to the false conjecture.
    The witness should be a tuple (W1, W2, P, T) or (P, T) where:
      - W1, W2 are matrices whose columns span the subspaces W_1 and W_2.
      - P, T are square matrices representing the operators.
    """
    try:
        if len(witness) == 4:
            W1, W2, P, T = witness
        elif len(witness) == 2:
            P, T = witness
            W1_cols = P.columnspace()
            W1 = sympy.Matrix.hstack(*W1_cols) if W1_cols else sympy.zeros(P.rows, 1)
            W2_cols = P.nullspace()
            W2 = sympy.Matrix.hstack(*W2_cols) if W2_cols else sympy.zeros(P.rows, 1)
        else:
            return [False, False, False, False]

        # H1: V is a vector space
        # We check if P and T are square matrices of the same size, and W1, W2 have matching row dimensions.
        n = P.rows
        h1 = (P.cols == n and T.rows == n and T.cols == n and W1.rows == n and W2.rows == n)

        if not h1:
            return [False, False, False, False]

        # H2: P is the projection operator onto W_1 along W_2
        # In the context of the false conjecture, this is interpreted as Im(P) = W_1 and Ker(P) = W_2.
        # (The dropped hypothesis was that P is idempotent / V = W_1 \oplus W_2).
        rank_p = P.rank()
        rank_w1 = W1.rank()
        rank_w2 = W2.rank()
        
        im_p_eq_w1 = (sympy.Matrix.hstack(P, W1).rank() == rank_p == rank_w1)
        ker_p_eq_w2 = (P * W2 == sympy.zeros(n, W2.cols) and (n - rank_p) == rank_w2)
        h2 = bool(im_p_eq_w1 and ker_p_eq_w2)

        # H3: T: V \to V is a linear operator
        # True by virtue of T being an n x n matrix (checked in H1).
        h3 = True

        # Conclusion: Both W_1 and W_2 are T-invariant if and only if T commutes with P
        # W_1 is T-invariant iff T(W_1) is a subset of W_1
        w1_inv = (sympy.Matrix.hstack(W1, T * W1).rank() == rank_w1)
        w2_inv = (sympy.Matrix.hstack(W2, T * W2).rank() == rank_w2)
        
        tp_eq_pt = (T * P == P * T)
        
        conclusion = ((w1_inv and w2_inv) == tp_eq_pt)
        neg_q = not conclusion

        return [h1, h2, h3, neg_q]

    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: P is the projection operator onto W_1 along W_2",
    "H_3: T is a linear operator",
    "¬Q: It is NOT the case that (Both W_1 and W_2 are T-invariant iff TP = PT)"
]

N_HYP = 3
NEG_Q_INDEX = 3
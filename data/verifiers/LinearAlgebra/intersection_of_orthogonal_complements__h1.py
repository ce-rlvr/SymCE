import sympy as sp

# Top-level setup for standard algebra objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple or list: (B, W1, W2)
    where B is an n x n sympy Matrix representing the bilinear form,
    and W1, W2 are subspaces represented as lists of vectors or matrices.
    """
    # Extract B, W1, W2
    try:
        if isinstance(witness, dict):
            B = witness.get('B')
            W1 = witness.get('W1')
            W2 = witness.get('W2')
            if B is None or W1 is None or W2 is None:
                return [False, False, False]
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            B, W1, W2 = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: B is a bilinear form on V
    try:
        if not isinstance(B, sp.Matrix):
            try:
                B = sp.Matrix(B)
            except Exception:
                pass
        if isinstance(B, sp.Matrix) and B.rows == B.cols:
            h1 = True
            n = B.rows
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: W_1 and W_2 are subspaces of V
    try:
        if not h1:
            h2 = False
        else:
            def parse_subspace(W, n):
                if isinstance(W, sp.Matrix):
                    if W.cols == n:
                        return W.T
                    elif W.rows == n:
                        return W
                    else:
                        raise ValueError("Matrix dimensions do not match n")
                elif isinstance(W, (list, tuple)):
                    if len(W) == 0:
                        return sp.zeros(n, 0)
                    cols = []
                    for v in W:
                        if isinstance(v, sp.Matrix):
                            if v.rows == n and v.cols == 1:
                                cols.append(v)
                            elif v.rows == 1 and v.cols == n:
                                cols.append(v.T)
                            else:
                                raise ValueError("Vector dimensions do not match n")
                        elif isinstance(v, (list, tuple)):
                            if len(v) == n:
                                cols.append(sp.Matrix(n, 1, v))
                            else:
                                raise ValueError("List dimensions do not match n")
                        else:
                            raise ValueError("Unknown vector type")
                    if cols:
                        return sp.Matrix.hstack(*cols)
                    else:
                        return sp.zeros(n, 0)
                else:
                    raise ValueError("Unknown subspace type")

            M1 = parse_subspace(W1, n)
            M2 = parse_subspace(W2, n)
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The orthogonal complement identity fails
    # We check both (W1 + W2)^perp == W1^perp \cap W2^perp 
    # and (W1 \cap W2)^perp == W1^perp + W2^perp
    # If either fails, the standard theorem conclusion fails.
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            def perp(M, B):
                if M.cols == 0:
                    return sp.eye(B.rows)
                ns = (M.T * B).nullspace()
                if not ns:
                    return sp.zeros(B.rows, 0)
                return sp.Matrix.hstack(*ns)

            def intersect(M1, M2):
                if M1.cols == 0 or M2.cols == 0:
                    return sp.zeros(M1.rows, 0)
                M12 = sp.Matrix.hstack(M1, -M2)
                ns = M12.nullspace()
                if not ns:
                    return sp.zeros(M1.rows, 0)
                k1 = M1.cols
                res = []
                for vec in ns:
                    x = vec[:k1, :]
                    res.append(M1 * x)
                if not res:
                    return sp.zeros(M1.rows, 0)
                return sp.Matrix.hstack(*res)

            def add(M1, M2):
                return sp.Matrix.hstack(M1, M2)

            def is_equal(M1, M2):
                r1 = M1.rank()
                r2 = M2.rank()
                if r1 != r2:
                    return False
                r12 = sp.Matrix.hstack(M1, M2).rank()
                return r12 == r1

            # Check (W1 + W2)^perp == W1^perp \cap W2^perp
            W1_plus_W2 = add(M1, M2)
            perp_sum = perp(W1_plus_W2, B)

            perp_W1 = perp(M1, B)
            perp_W2 = perp(M2, B)
            int_perps = intersect(perp_W1, perp_W2)

            eq1 = is_equal(perp_sum, int_perps)

            # Check (W1 \cap W2)^perp == W1^perp + W2^perp
            W1_int_W2 = intersect(M1, M2)
            perp_int = perp(W1_int_W2, B)
            sum_perps = add(perp_W1, perp_W2)

            eq2 = is_equal(perp_int, sum_perps)

            # The conjecture states the identity holds. We negate it.
            q = eq1 and eq2
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: B is a bilinear form on V",
    "H_2: W_1 and W_2 are subspaces of V",
    "¬Q: Orthogonal complement identity fails"
]

N_HYP = 2
NEG_Q_INDEX = 2
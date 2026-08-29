import sympy as sp

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (u, v) or (u, v, A).
    """
    if isinstance(witness, tuple):
        if len(witness) == 2:
            u, v = witness
            try:
                n = u.rows
                A = sp.eye(n) + u * v.T
            except Exception:
                A = None
        elif len(witness) == 3:
            u, v, A = witness
        else:
            return [False, False, False]
    else:
        return [False, False, False]

    # H_1: u and v are n x 1 column vectors
    try:
        h1 = isinstance(u, sp.MatrixBase) and isinstance(v, sp.MatrixBase) and \
             u.cols == 1 and v.cols == 1 and u.rows == v.rows
    except Exception:
        h1 = False

    # H_2: A = I_n + u v^T
    try:
        n = u.rows
        h2 = (A == sp.eye(n) + u * v.T)
    except Exception:
        h2 = False

    # ¬Q: The characteristic polynomial of A is NOT (x-1)^{n-1}(x - 1 - v^T u)
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            x = sp.Symbol('x')
            p_A = A.charpoly(x).as_expr()
            
            if n == 0:
                # For n=0, the formula gives (x-1)^{-1}(x-1), which has a negative exponent
                # and is therefore not syntactically a polynomial.
                neg_q = True
            else:
                vTu = (v.T * u)[0, 0]
                expected_p = ((x - 1)**(n - 1)) * (x - 1 - vTu)
                diff = sp.simplify(sp.expand(p_A - expected_p))
                neg_q = diff != 0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: u and v are n x 1 column vectors",
    "H_2: A = I_n + u v^T",
    "¬Q: The characteristic polynomial of A is not (x-1)^{n-1}(x - 1 - v^T u)"
]

N_HYP = 2
NEG_Q_INDEX = 2
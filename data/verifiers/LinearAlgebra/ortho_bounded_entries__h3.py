import sympy

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok].
    """
    # H_1: Q is an n x n matrix with real entries
    # Note: The true theorem requires real entries. The dropped hypothesis was "real entries",
    # so a valid counterexample must be a complex matrix. We check if it's a square matrix
    # to allow the complex counterexample to pass this remaining structural hypothesis.
    h1_ok = False
    Q = None
    try:
        Q = sympy.Matrix(witness)
        if Q.is_square:
            h1_ok = True
    except Exception:
        pass

    # H_2: Q is an orthogonal matrix (Q^T * Q = I)
    h2_ok = False
    try:
        if h1_ok and Q is not None:
            n = Q.shape[0]
            prod = Q.T * Q
            I = sympy.eye(n)
            diff = sympy.simplify(prod - I)
            
            if diff == sympy.zeros(n, n):
                h2_ok = True
            else:
                # Fallback for numerical evaluation if symbolic simplification fails
                is_zero = True
                for i in range(n):
                    for j in range(n):
                        val = diff[i, j].evalf()
                        try:
                            if abs(complex(val)) > 1e-9:
                                is_zero = False
                                break
                        except TypeError:
                            is_zero = False
                            break
                    if not is_zero:
                        break
                h2_ok = is_zero
    except Exception:
        pass

    # ¬Q: The absolute value of q_{ij} is greater than 1 for some i, j
    neg_q_ok = False
    try:
        if h1_ok and Q is not None:
            n = Q.shape[0]
            for i in range(n):
                for j in range(n):
                    val = Q[i, j]
                    try:
                        abs_val = sympy.Abs(val).evalf()
                        # Try numerical float comparison first
                        try:
                            if float(abs_val) > 1.0 + 1e-9:
                                neg_q_ok = True
                                break
                        except TypeError:
                            # Fallback to symbolic relational check
                            if sympy.simplify(abs_val > 1) == True:
                                neg_q_ok = True
                                break
                    except Exception:
                        pass
                if neg_q_ok:
                    break
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Q is an n x n matrix with real entries",
    "H_2: Q is an orthogonal matrix",
    "¬Q: The absolute value of q_{ij} is greater than 1 for some i, j"
]

N_HYP = 2
NEG_Q_INDEX = 2
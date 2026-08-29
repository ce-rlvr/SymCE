import sympy as sp

# Top-level setup: named object bindings
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if it falsifies the conclusion of the conjecture.
    
    The witness is expected to be a tuple (A, B).
    """
    try:
        A = witness[0]
        B = witness[1]
    except Exception:
        return [False, False, False]
    
    # H_1: B is an n x m matrix over F
    try:
        if isinstance(B, sp.MatrixBase):
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: AB and BA are square matrices
    try:
        AB = A * B
        BA = B * A
        if isinstance(AB, sp.MatrixBase) and isinstance(BA, sp.MatrixBase):
            if AB.rows == AB.cols and BA.rows == BA.cols:
                h2_ok = True
            else:
                h2_ok = False
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion t^n * p_AB(t) == t^m * p_BA(t) FAILS
    try:
        if h1_ok and h2_ok:
            n, m = B.shape
            t = sp.Symbol('t')
            
            # Compute characteristic polynomials
            p_AB = AB.charpoly(t).as_expr()
            p_BA = BA.charpoly(t).as_expr()
            
            # Evaluate t^n * p_AB(t) and t^m * p_BA(t)
            lhs = sp.expand(t**n * p_AB)
            rhs = sp.expand(t**m * p_BA)
            
            # Check if they are NOT equal
            diff = sp.expand(lhs - rhs)
            neg_q_ok = bool(diff != 0)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: B is a matrix over F",
    "H_2: AB and BA are square matrices",
    "¬Q: t^n p_{AB}(t) != t^m p_{BA}(t)"
]

N_HYP = 2
NEG_Q_INDEX = 2
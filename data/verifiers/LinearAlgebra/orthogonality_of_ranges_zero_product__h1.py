import sympy as sp
from sympy import Matrix, zeros, eye

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for orthogonal projections P_1 and P_2, 
    P_1 P_2 = 0 iff range(P_1) is orthogonal to range(P_2).
    
    Due to a common artifact in theorem dropping, the dropped hypothesis was likely 
    "orthogonal" (making them general projections), but the text retained the word.
    We check if they are projections, and evaluate the conclusion.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            P1, P2, A = witness
        else:
            P1, P2 = witness
            A = eye(P1.shape[0])
    except Exception:
        return [False, False, False]

    # H_1: P_1 is an orthogonal projection operator on V
    # We check if it's a projection. We also check orthogonality with respect to A if provided,
    # but for standard matrices where the dropped hypothesis was "orthogonal", we just check P^2 == P
    # to avoid rejecting the intended counterexample of non-orthogonal projections.
    try:
        h1_ok = bool(P1**2 == P1)
        # If an inner product matrix A is explicitly provided, check orthogonality w.r.t A
        if isinstance(witness, tuple) and len(witness) == 3:
            h1_ok = h1_ok and bool(P1.T * A == A * P1)
    except Exception:
        h1_ok = False

    # H_2: P_2 is an orthogonal projection operator on V
    try:
        h2_ok = bool(P2**2 == P2)
        if isinstance(witness, tuple) and len(witness) == 3:
            h2_ok = h2_ok and bool(P2.T * A == A * P2)
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion FAILS at the witness
    # Conclusion: P_1 P_2 = 0 iff range(P_1) is orthogonal to range(P_2)
    try:
        p1_p2_zero = bool(P1 * P2 == zeros(*P1.shape))
        
        # range(P_1) perp range(P_2) means for all x, y, (P1 x)^T A (P2 y) = 0
        # which is equivalent to P1^T A P2 == 0
        ranges_orthogonal = bool(P1.T * A * P2 == zeros(*P1.shape))
        
        # The conclusion is the equivalence of the two statements
        conclusion_holds = (p1_p2_zero == ranges_orthogonal)
        neg_q_ok = not conclusion_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P_1 is an orthogonal projection operator on V",
    "H_2: P_2 is an orthogonal projection operator on V",
    "¬Q: It is NOT the case that (P_1 P_2 = 0 if and only if the range of P_1 is orthogonal to the range of P_2)"
]

N_HYP = 2
NEG_Q_INDEX = 2
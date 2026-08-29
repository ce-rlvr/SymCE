import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample.
    Returns a list of booleans corresponding to the remaining hypotheses and the negated conclusion.
    """
    # Determine if witness is just a matrix P or a tuple (P, x)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            P, x = witness
            is_tuple = True
        else:
            P = witness
            is_tuple = False

        # H_1: V is an inner product space over R or C
        # We interpret this as the witness providing a valid square matrix representing an operator.
        h1 = isinstance(P, Matrix) and P.is_square
    except Exception:
        h1 = False

    # H_2: P^2 = P
    try:
        if h1:
            diff = P**2 - P
            h2 = all(sp.simplify(val) == 0 for val in diff)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: P = P^*
    try:
        if h1:
            diff = P - P.H
            h3 = all(sp.simplify(val) == 0 for val in diff)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: There exists x in V such that <Px, x> < 0
    # (i.e., the conclusion <Px, x> >= 0 for all x FAILS)
    try:
        if not h1:
            neg_q = False
        elif is_tuple:
            if isinstance(x, Matrix) and x.shape == (P.rows, 1):
                val = sp.simplify((x.H * P * x)[0, 0])
                if val.is_real is False:
                    neg_q = True
                else:
                    neg_q = float(sp.re(val)) < -1e-9
            else:
                neg_q = False
        else:
            is_real_matrix = True
            for val in P:
                if val.is_real is False:
                    is_real_matrix = False
                    break
            
            # If P is complex and not Hermitian, <Px, x> is not always real, hence not always >= 0
            if not is_real_matrix and not h3:
                neg_q = True
            else:
                # Check if the symmetric/Hermitian part is positive semi-definite
                sym_P = (P + P.H) / 2
                evs = sym_P.eigenvals()
                neg_q = False
                for val in evs:
                    if float(sp.re(val)) < -1e-9:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is an inner product space over R or C",
    "H_2: P^2 = P",
    "H_3: P = P^*",
    "¬Q: There exists x in V such that <Px, x> < 0"
]

N_HYP = 3
NEG_Q_INDEX = 3
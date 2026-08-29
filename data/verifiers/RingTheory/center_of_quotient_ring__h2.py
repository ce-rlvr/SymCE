import sympy
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    "The image \\pi(Z(R)) is contained in the center of R/I."
    
    The dropped hypothesis from the true theorem is that I must be a two-sided ideal.
    If I is not a two-sided ideal, R/I is not a ring, so it does not have a center,
    and the conclusion fails.
    """
    try:
        if len(witness) == 2:
            R, I = witness
            Z_R = None
        elif len(witness) == 3:
            R, I, Z_R = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a ring
    h1 = False
    try:
        if R:
            closed_add = all((a + b) in R for a in R for b in R)
            closed_mul = all((a * b) in R for a in R for b in R)
            if closed_add and closed_mul:
                zeros_R = [z for z in R if all((a + z) == a for a in R)]
                if zeros_R:
                    z = zeros_R[0]
                    has_inv = all(any((a + b) == z for b in R) for a in R)
                    assoc_add = all(((a + b) + c) == (a + (b + c)) for a in R for b in R for c in R)
                    comm_add = all((a + b) == (b + a) for a in R for b in R)
                    assoc_mul = all(((a * b) * c) == (a * (b * c)) for a in R for b in R for c in R)
                    dist_left = all((a * (b + c)) == (a * b + a * c) for a in R for b in R for c in R)
                    dist_right = all(((a + b) * c) == (a * c + b * c) for a in R for b in R for c in R)
                    if has_inv and assoc_add and comm_add and assoc_mul and dist_left and dist_right:
                        h1 = True
    except Exception:
        pass

    # H_2: \pi: R -> R/I is the canonical projection
    # This implies I is an additive subgroup of R
    h2 = False
    try:
        if I and all(i in R for i in I):
            closed_add_I = all((a + b) in I for a in I for b in I)
            if closed_add_I:
                zeros_I = [z for z in I if all((a + z) == a for a in I)]
                if zeros_I:
                    z_I = zeros_I[0]
                    has_inv_I = all(any((a + b) == z_I for b in I) for a in I)
                    h2 = has_inv_I
    except Exception:
        pass

    # H_3: Z(R) is the center of R
    h3 = False
    try:
        actual_center = [a for a in R if all((a * b) == (b * a) for b in R)]
        if Z_R is not None:
            if len(Z_R) == len(actual_center) and all(z in actual_center for z in Z_R):
                h3 = True
        else:
            h3 = True
    except Exception:
        pass

    # ¬Q: The image \pi(Z(R)) is not contained in the center of R/I
    # The conclusion holds universally if I is a two-sided ideal (since R/I is then a valid ring).
    # It fails if I is not a two-sided ideal, because R/I is not a ring and thus has no center.
    neg_q = False
    try:
        is_ideal = True
        for i in I:
            for r in R:
                if (i * r) not in I:
                    is_ideal = False
                    break
                if (r * i) not in I:
                    is_ideal = False
                    break
            if not is_ideal:
                break
        neg_q = not is_ideal
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: \\pi: R -> R/I is the canonical projection",
    "H_3: Z(R) is the center of R",
    "¬Q: The image \\pi(Z(R)) is not contained in the center of R/I"
]

N_HYP = 3
NEG_Q_INDEX = 3
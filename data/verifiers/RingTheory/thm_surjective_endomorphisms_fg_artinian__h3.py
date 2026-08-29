import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be a right Artinian ring, and M a finitely generated right R-module. 
    Let f: M -> M be an endomorphism. Then f is an injective homomorphism."
    
    A valid witness is an endomorphism (represented by a square matrix over a field)
    that is not injective (determinant is zero).
    """
    # Extract matrix if witness is provided as a tuple (e.g., (R, M, f))
    if isinstance(witness, tuple):
        for item in witness:
            if isinstance(item, sympy.Matrix):
                f = item
                break
        else:
            f = witness
    else:
        f = witness

    try:
        # H_1: R is a right Artinian ring.
        # If f is a matrix of numbers, we can consider its base ring to be a field 
        # (e.g., Q, R, or C), which is an Artinian ring.
        h1_ok = isinstance(f, sympy.Matrix) and all(e.is_number for e in f)
    except Exception:
        h1_ok = False

    try:
        # H_2: M is a finitely generated right R-module.
        # A finite square matrix represents an endomorphism of a finitely generated free module.
        h2_ok = isinstance(f, sympy.Matrix) and f.is_square and f.shape[0] > 0
    except Exception:
        h2_ok = False

    try:
        # ¬Q: f is not an injective homomorphism (and thus not an isomorphism).
        # For an endomorphism of a finite-dimensional vector space, it is not injective 
        # if and only if its determinant is zero.
        neg_q_ok = bool(f.det() == 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "H_2: M is a finitely generated right R-module",
    "¬Q: f is not an injective homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2
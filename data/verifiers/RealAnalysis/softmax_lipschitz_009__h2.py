import math
import sympy
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and the negated conclusion.
    The witness is expected to be the dimension n.
    """
    try:
        # Extract n from the witness
        if isinstance(witness, (tuple, list)):
            n_val = witness[0]
        else:
            n_val = witness
            
        # Check if n is a positive integer
        if isinstance(n_val, int) or (isinstance(n_val, float) and n_val.is_integer()):
            n = int(n_val)
            h1 = (n >= 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    # The conclusion states that the softmax function is globally Lipschitz continuous on R^n.
    # Mathematically, the Jacobian of the softmax function is J = diag(s) - s*s^T, where s = softmax(x).
    # Since s_i in (0, 1) and sum(s_i) = 1, the entries of J are uniformly bounded for any x in R^n.
    # Therefore, the spectral norm (and thus the Euclidean operator norm) of J is bounded, 
    # meaning the softmax function is ALWAYS globally Lipschitz continuous on R^n for any n >= 1.
    # Because the conclusion is universally true, it never fails.
    # Thus, the negated conclusion is always False.
    neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The softmax function is not globally Lipschitz continuous on R^n"
]

N_HYP = 1
NEG_Q_INDEX = 1
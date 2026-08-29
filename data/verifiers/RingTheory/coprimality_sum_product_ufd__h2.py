import sympy as sp
from sympy import gcd, MatrixBase, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Given a witness, checks if it satisfies the hypotheses and fails the conclusion.
    The witness is expected to contain the elements a and b.
    """
    # Extract a and b from the witness
    if isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            a, b = witness
        elif len(witness) >= 3:
            # If witness includes the ring R, e.g., (R, a, b), take the last two
            a, b = witness[-2], witness[-1]
        else:
            return [False, False, False]
    elif isinstance(witness, dict) and 'a' in witness and 'b' in witness:
        a = witness['a']
        b = witness['b']
    else:
        return [False, False, False]
        
    # H_1: Let R be a unique factorization domain.
    try:
        # Matrices do not form a UFD. Standard sympy scalars/polynomials are treated as being in a UFD.
        if isinstance(a, MatrixBase) or isinstance(b, MatrixBase):
            h1_ok = False
        else:
            h1_ok = True
    except Exception:
        h1_ok = False
        
    # H_2: The greatest common divisor of a and b is 1.
    try:
        g = gcd(a, b)
        h2_ok = bool(g == 1 or g == -1)
    except Exception:
        h2_ok = False
        
    # ¬Q: The greatest common divisor of a+b and ab is NOT 1.
    try:
        g_ab = gcd(a + b, a * b)
        neg_q_ok = bool(g_ab != 1 and g_ab != -1)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: The greatest common divisor of a and b is 1",
    "¬Q: The greatest common divisor of a+b and ab is not 1"
]

N_HYP = 2
NEG_Q_INDEX = 2
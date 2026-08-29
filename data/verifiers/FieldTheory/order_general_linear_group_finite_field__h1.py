import sympy
from sympy.ntheory import factorint

# Top-level setup for potential witness expressions
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should provide the matrix dimension `n` and the field size `q`.
    """
    try:
        # Parse witness
        if isinstance(witness, dict):
            if 'q' not in witness:
                return [False, False, False]
            n = witness.get('n', 2)
            q = witness['q']
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                n, q = witness
            else:
                return [False, False, False]
        elif isinstance(witness, int):
            # Fallback if only q is provided
            n = 2
            q = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n >= 1
    except Exception:
        h1 = False

    # H_2: q is an integer >= 2 (so that a structure of size q can exist)
    try:
        h2 = isinstance(q, int) and q >= 2
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails at the witness.
    # The formula q^{n(n-1)/2} \prod_{i=1}^n (q^i - 1) gives the correct order of GL_n(F_q) 
    # if and only if F_q is a valid finite field (i.e., q is a prime power).
    # If q is not a prime power, F_q is not a field (or if interpreted as Z/qZ, the order differs),
    # meaning the conclusion fails.
    try:
        if h1 and h2:
            factors = factorint(q)
            is_prime_power = (len(factors) == 1)
            neg_q = not is_prime_power
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: q is an integer >= 2",
    "¬Q: The order of GL_n(F_q) is not given by the formula (q is not a prime power)"
]

N_HYP = 2
NEG_Q_INDEX = 2
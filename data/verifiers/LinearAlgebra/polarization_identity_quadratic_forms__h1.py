import sympy
from sympy import Matrix, eye, zeros
from sympy.ntheory import isprime

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to represent a quadratic form over a field GF(p).
    It can be provided as a tuple (M, p), a dict {'M': M, 'p': p}, just a prime p, 
    or just a Matrix M (defaulting to p=2).
    """
    try:
        if isinstance(witness, dict):
            M = witness.get('M', I2)
            p = witness.get('p', 2)
        elif isinstance(witness, tuple) and len(witness) == 2:
            M, p = witness
        elif isinstance(witness, int):
            M = I2
            p = witness
        elif isinstance(witness, Matrix):
            M = witness
            p = 2
        else:
            return [False, False]
            
        # H_1: q is a quadratic form on V.
        # We verify this by checking if M is a valid square matrix and p is a prime (defining GF(p)).
        h1 = isinstance(M, Matrix) and M.is_square and M.shape[0] > 0 and isprime(p)
    except Exception:
        h1 = False

    try:
        # ¬Q: The symmetric bilinear form B is NOT uniquely recovered by B(x,y) = (1/2)(q(x+y) - q(x) - q(y)).
        # In a field of characteristic 2, the element 1/2 is undefined (2 is not invertible),
        # so the polarization identity fails to recover B.
        neg_q = (p == 2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: q is a quadratic form on V (represented by matrix M over GF(p))",
    "¬Q: The polarization identity fails to uniquely recover B (e.g. 1/2 is undefined in char 2)"
]

N_HYP = 1
NEG_Q_INDEX = 1
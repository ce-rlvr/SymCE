import sympy
import sympy.ntheory

# Standard bindings for rings Z/nZ
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness):
    """
    Checks if the given witness (representing the characteristic n of the ring Z/nZ)
    is a valid counterexample to the conjecture.
    """
    # Extract the primary witness if provided as a tuple/list
    if isinstance(witness, (tuple, list)) and len(witness) > 0:
        witness = witness[0]
        
    # Parse string representations like "Z/6Z" or "Z6"
    if isinstance(witness, str):
        digits = ''.join(filter(str.isdigit, witness))
        if digits:
            witness = int(digits)

    try:
        n = int(witness)
        # H_1: F is a commutative ring (n >= 2 ensures Z/nZ is a valid ring)
        h1 = (n >= 2)
    except Exception:
        h1 = False

    try:
        n = int(witness)
        # ¬Q: R/I is NOT an integral domain.
        # R/I is an integral domain iff F is an integral domain.
        # For F = Z/nZ, it is an integral domain iff n is prime.
        # Therefore, R/I is not an integral domain iff n is composite.
        neg_q = (n >= 2) and not sympy.ntheory.isprime(n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a commutative ring (witness n >= 2 represents Z/nZ)",
    "¬Q: R/I is not an integral domain"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy

# Top-level setup
# The witness is expected to be an integer n, representing the ring R = Z,
# the quotient ring F = Z/nZ, and the natural projection f: Z -> Z/nZ.

def conditions(witness) -> list[bool]:
    try:
        # Extract the integer n from the witness
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            n = int(witness[0])
        else:
            n = int(witness)
    except Exception:
        return [False, False, False]

    try:
        # H_1: R is a commutative ring with identity
        # R = Z is a commutative ring with identity.
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        # H_2: f: R -> F is a surjective ring homomorphism
        # The natural projection f: Z -> Z/nZ is a surjective ring homomorphism.
        h2_ok = True
    except Exception:
        h2_ok = False

    try:
        # ¬Q: The kernel of f is not a maximal ideal of R
        # The kernel of f is nZ.
        # In Z, the ideal nZ is maximal if and only if |n| is prime.
        # Thus, the conclusion fails (neg_Q is True) if |n| is not prime.
        neg_q_ok = not sympy.isprime(abs(n))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f: R -> F is a surjective ring homomorphism",
    "¬Q: The kernel of f is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2
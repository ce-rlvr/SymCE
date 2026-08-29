import sympy
from sympy.ntheory import factorint

# Top-level setup: named object bindings
# We represent the ring Z/nZ as the integer n. Z is represented as 0.
Z = 0
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    try:
        # Witness can be a tuple (n, m) representing R = Z/nZ and S = Z/mZ
        # with the natural projection f: Z/nZ -> Z/mZ.
        # If a single value is provided, we assume R = S and f is the identity.
        if isinstance(witness, tuple) and len(witness) == 2:
            n_raw, m_raw = witness
        else:
            n_raw = m_raw = witness
            
        def parse_ring(r):
            if str(r) in ('ZZ', 'Z', 'Integers'):
                return 0
            return int(r)
            
        n = parse_ring(n_raw)
        m = parse_ring(m_raw)
    except Exception:
        return [False, False, False, False, False]

    # H1: R is a commutative ring with identity
    try:
        h1 = (n >= 0)
    except Exception:
        h1 = False

    # H2: S is a commutative ring with identity
    try:
        h2 = (m >= 0)
    except Exception:
        h2 = False

    # H3: S is not the zero ring
    try:
        h3 = (m != 1)
    except Exception:
        h3 = False

    # H4: f is a surjective ring homomorphism from R to S
    try:
        if n == 0:
            # Natural projection from Z to Z/mZ is always a surjective ring homomorphism
            h4 = True
        elif n > 0 and m > 0 and n % m == 0:
            # Natural projection from Z/nZ to Z/mZ is well-defined and surjective iff m divides n
            h4 = True
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: S is not a local ring
    try:
        if m == 0:
            # Z is not a local ring (it has infinitely many maximal ideals)
            neg_q = True
        elif m == 1:
            # The zero ring is not a local ring
            neg_q = True
        else:
            # Z/mZ is a local ring iff m is a prime power (exactly one prime factor)
            factors = factorint(m)
            is_local = (len(factors) == 1)
            neg_q = not is_local
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a commutative ring with identity",
    "H_3: S is not the zero ring",
    "H_4: f is a surjective ring homomorphism from R to S",
    "¬Q: S is not a local ring"
]

N_HYP = 4
NEG_Q_INDEX = 4
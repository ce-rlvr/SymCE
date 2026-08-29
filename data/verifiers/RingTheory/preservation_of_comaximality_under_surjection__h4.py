import math

# Top-level setup
# We represent rings R and S as Z/nZ and Z/mZ, where n, m >= 0.
# A witness is a tuple (n, m, a, b) where:
#   n: modulus for ring R (0 means Z)
#   m: modulus for ring S (0 means Z)
#   a: generator for ideal I in R
#   b: generator for ideal J in R
# The homomorphism f: R -> S is the natural projection, which is well-defined
# and surjective iff m divides n (with the convention that 0 divides 0).

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        n, m, a, b = witness
    except Exception:
        return [False, False, False, False]

    # H_1: R and S are rings
    try:
        h1 = type(n) is int and type(m) is int and n >= 0 and m >= 0
    except Exception:
        h1 = False

    # H_2: f: R -> S is a surjective ring homomorphism
    try:
        if m == 0:
            h2 = (n == 0)
        else:
            h2 = (n % m == 0)
    except Exception:
        h2 = False

    # H_3: I and J are ideals of R
    try:
        h3 = type(a) is int and type(b) is int
    except Exception:
        h3 = False

    # ¬Q: f(I) and f(J) are not comaximal in S
    try:
        if m == 0:
            is_comaximal = (math.gcd(a, b) == 1)
        else:
            # In Z/mZ, ideals (a) and (b) are comaximal iff gcd(a, b, m) == 1
            is_comaximal = (math.gcd(math.gcd(a, b), m) == 1)
        neg_q = not is_comaximal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a surjective ring homomorphism",
    "H_3: I and J are ideals of R",
    "¬Q: f(I) and f(J) are not comaximal in S"
]

N_HYP: int = 3
NEG_Q_INDEX: int = 3
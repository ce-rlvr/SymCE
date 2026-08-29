import sympy

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        h1 = True
    except Exception:
        h1 = False

    try:
        n = int(witness)
        is_prime_ideal = sympy.isprime(abs(n)) or n == 0
        neg_q = not is_prime_ideal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "not Q: The ideal P polynomials is not a prime ideal in R polynomials"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy.ntheory import totient

# Top-level setup
# (No specific named objects required for this integer-witness conjecture)

def conditions(witness) -> list[bool]:
    """
    Given a witness (an integer n), checks if it satisfies the hypotheses
    and falsifies the conclusion of the conjecture.
    """
    # H_1: \zeta_n is a primitive n-th root of unity in \mathbb{C}
    # This is well-defined for any positive integer n.
    try:
        h1 = isinstance(witness, int) and witness >= 1
    except Exception:
        h1 = False

    # H_2: \zeta_{2n} is a primitive 2n-th root of unity in \mathbb{C}
    # This is well-defined for any positive integer 2n.
    try:
        h2 = isinstance(witness, int) and (2 * witness) >= 1
    except Exception:
        h2 = False

    # ¬Q: The cyclotomic fields \mathbb{Q}(\zeta_n) and \mathbb{Q}(\zeta_{2n}) are NOT equal.
    try:
        if isinstance(witness, int) and witness >= 1:
            # \mathbb{Q}(\zeta_n) is always a subfield of \mathbb{Q}(\zeta_{2n}) since \zeta_n = (\zeta_{2n})^2.
            # Therefore, the two fields are equal if and only if their degrees over \mathbb{Q} are equal.
            # The degree of \mathbb{Q}(\zeta_k) over \mathbb{Q} is given by Euler's totient function \phi(k).
            # We want the negation of the conclusion, meaning the degrees must be DIFFERENT.
            neg_q = bool(totient(witness) != totient(2 * witness))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: zeta_n is a primitive n-th root of unity in C",
    "H_2: zeta_2n is a primitive 2n-th root of unity in C",
    "¬Q: The cyclotomic fields Q(zeta_n) and Q(zeta_2n) are not equal"
]

N_HYP = 2
NEG_Q_INDEX = 2
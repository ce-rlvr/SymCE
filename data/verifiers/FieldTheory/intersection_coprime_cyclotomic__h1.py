import sympy
from sympy import gcd

# Top-level setup
# No special named objects needed for this domain.

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion at the given witness.
    
    The witness is expected to be a tuple (n, m) representing the orders of the roots of unity.
    (The primitive roots themselves are implicitly determined by n and m).
    
    Returns:
        [H_1_ok, H_2_ok, H_3_ok, neg_Q_ok]
    """
    try:
        n, m = witness
    except Exception:
        return [False, False, False, False]

    # H_1: n and m are coprime
    try:
        h1_ok = (gcd(n, m) == 1)
    except Exception:
        h1_ok = False

    # H_2: ζ_n is a primitive n-th root of unity
    # This is true by definition for any valid integer n >= 1.
    try:
        h2_ok = isinstance(n, int) and n >= 1
    except Exception:
        h2_ok = False

    # H_3: ζ_m is a primitive m-th root of unity
    # This is true by definition for any valid integer m >= 1.
    try:
        h3_ok = isinstance(m, int) and m >= 1
    except Exception:
        h3_ok = False

    # ¬Q: The intersection of the fields ℚ(ζ_n) ∩ ℚ(ζ_m) is NOT ℚ.
    # The intersection of ℚ(ζ_n) and ℚ(ζ_m) is ℚ(ζ_{gcd(n,m)}).
    # If n and m are coprime, gcd(n, m) = 1, so the intersection is ℚ(ζ_1) = ℚ.
    # Therefore, the intersection is ALWAYS ℚ when n and m are coprime.
    # The negated conclusion is True if the intersection is NOT ℚ.
    # Since the intersection is always ℚ for coprime n and m, this will always be False for valid witnesses.
    # (The conjecture is actually true, but we follow the contract to evaluate the negation).
    try:
        intersection_degree = sympy.totient(gcd(n, m))
        neg_q_ok = (intersection_degree > 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n and m are coprime",
    "H_2: ζ_n is a primitive n-th root of unity",
    "H_3: ζ_m is a primitive m-th root of unity",
    "¬Q: The intersection of the fields ℚ(ζ_n) ∩ ℚ(ζ_m) is not ℚ"
]

N_HYP = 3
NEG_Q_INDEX = 3
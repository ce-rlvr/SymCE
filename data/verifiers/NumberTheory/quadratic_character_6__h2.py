import sympy
from sympy.ntheory import isprime, legendre_symbol

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    """
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(witness))
    except Exception:
        h1 = False

    # neg_Q: The conclusion FAILS at the witness
    # Conclusion: (6/p) = 1 if and only if p = 1, 5, 19, 23 (mod 24)
    try:
        # Evaluate the Legendre symbol (6/p)
        # Note: For p=2, legendre_symbol raises a ValueError because it is only defined for odd primes.
        # This makes the conclusion ill-formed/fail for p=2.
        leg_sym = legendre_symbol(6, witness)
        left = (leg_sym == 1)
        right = (witness % 24 in [1, 5, 19, 23])
        q_holds = (left == right)
    except Exception:
        q_holds = False

    neg_q = not q_holds

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The equivalence (6/p) = 1 iff p ≡ 1, 5, 19, 23 (mod 24) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1
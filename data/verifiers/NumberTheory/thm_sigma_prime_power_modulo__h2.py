import sympy
import sympy.ntheory

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide values for p and k.
    """
    try:
        if isinstance(witness, dict):
            p = witness['p']
            k = witness['k']
        elif hasattr(witness, 'p') and hasattr(witness, 'k'):
            p = witness.p
            k = witness.k
        else:
            p, k = witness
    except Exception:
        return [False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # ¬Q: \sigma(p^k) \not\equiv 1 \pmod p
    try:
        val = p**k
        # If p^k is not a strictly positive integer, the sum of divisors is undefined
        # or not applicable in the standard sense, meaning the conclusion fails.
        if not isinstance(val, (int, sympy.Integer)) or val <= 0:
            neg_q = True
        else:
            sigma_val = sympy.ntheory.divisor_sigma(val)
            neg_q = bool((sigma_val % p) != 1)
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: \\sigma(p^k) \\not\\equiv 1 \\pmod p"
]

N_HYP = 1
NEG_Q_INDEX = 1
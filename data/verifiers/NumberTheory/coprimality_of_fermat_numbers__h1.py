import math
import sympy

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "For all non-negative integers n, m, gcd(F_n, F_m) = 1"
    where F_k = 2^{2^k} + 1 is the k-th Fermat number.
    """
    try:
        # Witness can be a dictionary or a tuple/list of two integers
        if isinstance(witness, dict):
            n = witness['n']
            m = witness['m']
        else:
            n, m = witness
        
        n = int(n)
        m = int(m)
        h1 = (n >= 0) and (m >= 0)
    except Exception:
        h1 = False

    try:
        # We restrict n and m to be < 20 to prevent memory/time exhaustion
        # since Fermat numbers grow extremely fast (double exponential).
        if h1 and n < 20 and m < 20:
            Fn = 2**(2**n) + 1
            Fm = 2**(2**m) + 1
            neg_q = math.gcd(Fn, Fm) != 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n and m are non-negative integers",
    "¬Q: gcd(F_n, F_m) != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
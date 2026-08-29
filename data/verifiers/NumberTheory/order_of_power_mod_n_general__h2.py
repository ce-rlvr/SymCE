import math
from sympy.ntheory import n_order
import sympy

# Top-level setup
# (No specific named objects required for this Number Theory conjecture)

def conditions(witness):
    """
    Given a witness, checks if it satisfies the hypotheses and falsifies the conclusion.
    The witness can be a dictionary {'a': a, 'n': n, 'k': k, 'm': m} or a tuple (a, n, k, m).
    If k is omitted in a tuple (a, n, m), it will be computed automatically.
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            n = witness['n']
            m = witness['m']
            k = witness.get('k', None)
        elif len(witness) == 4:
            a, n, k, m = witness
        elif len(witness) == 3:
            a, n, m = witness
            k = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: n is an integer greater than or equal to 2
    try:
        n_val = int(n)
        h1 = (n_val == n) and (n_val >= 2)
    except Exception:
        h1 = False

    # H2: The order of a modulo n is k
    try:
        a_val = int(a)
        actual_k = n_order(a_val, n_val)
        if k is None:
            k_val = actual_k
            h2 = True
        else:
            k_val = int(k)
            h2 = (actual_k == k_val)
    except Exception:
        h2 = False

    # H3: m is a positive integer
    try:
        m_val = int(m)
        h3 = (m_val == m) and (m_val > 0)
    except Exception:
        h3 = False

    # Conclusion: The order of a^m modulo n is equal to k / gcd(m, k)
    # We want neg_Q to be True when the conclusion FAILS.
    try:
        if h2 and h3:
            expected = k_val // math.gcd(m_val, k_val)
            actual = n_order(pow(a_val, m_val, n_val), n_val)
            neg_q = (actual != expected)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer greater than or equal to 2",
    "H_2: The order of a modulo n is k",
    "H_3: m is a positive integer",
    "¬Q: The order of a^m modulo n is NOT equal to k / gcd(m, k)"
]

N_HYP = 3
NEG_Q_INDEX = 3
import sympy
from sympy import divisors, totient, divisor_count

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: phi(n) denotes Euler's totient function",
    "H_3: d(n) denotes the number of divisors function",
    "¬Q: sum_{k|n} sigma(k) phi(n/k) != n * d(n)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    The conjecture is missing the hypothesis that defines sigma(n) as the sum of divisors.
    Without it, sigma is an undefined/arbitrary function, making the identity false.
    A valid witness should provide both n and a counterexample function/mapping for sigma.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, sigma = witness
        elif isinstance(witness, dict) and 'n' in witness and 'sigma' in witness:
            n = witness['n']
            sigma = witness['sigma']
        else:
            n = witness
            sigma = sympy.divisor_sigma
    except Exception:
        n = witness
        sigma = sympy.divisor_sigma

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n > 0
    except Exception:
        h1 = False

    # H_2: phi(n) denotes Euler's totient function (holds by evaluation context)
    h2 = True

    # H_3: d(n) denotes the number of divisors function (holds by evaluation context)
    h3 = True

    # ¬Q: The conclusion fails at the witness
    try:
        if not h1:
            neg_q = False
        else:
            divs = divisors(n)
            lhs = 0
            for k in divs:
                if callable(sigma):
                    val = sigma(k)
                elif isinstance(sigma, dict):
                    val = sigma[k]
                else:
                    val = sigma
                lhs += val * totient(n // k)
            
            rhs = n * divisor_count(n)
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]
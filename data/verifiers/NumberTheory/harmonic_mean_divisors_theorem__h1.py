import sympy

# Top-level setup
# No special bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        h1 = (n == witness)
    except Exception:
        h1 = False

    try:
        if not h1 or n == 0:
            neg_q = False
        else:
            divs = sympy.divisors(n)
            tau_n = len(divs)
            sigma_n = sum(divs)
            
            sum_inv = sum(sympy.Rational(1, d) for d in divs)
            harmonic_mean = sympy.Rational(tau_n, 1) / sum_inv
            
            formula = sympy.Rational(n * tau_n, sigma_n)
            
            neg_q = bool(harmonic_mean != formula)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: tau(n) is the number of divisors of n",
    "¬Q: The harmonic mean of the divisors of n is not equal to n*tau(n)/sigma(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy.ntheory import divisor_sigma, divisors

# No named bindings needed for number theory

def conditions(witness) -> list[bool]:
    try:
        n = sympy.sympify(witness)
        if n.is_integer is not True:
            return [False]
        
        sigma_n = divisor_sigma(n)
        divs = divisors(n)
        sum_nd = sum(n // d for d in divs)
        
        neg_q = bool(sigma_n != sum_nd)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sigma(n) != sum_{d|n} n/d"
]

N_HYP = 0
NEG_Q_INDEX = 0
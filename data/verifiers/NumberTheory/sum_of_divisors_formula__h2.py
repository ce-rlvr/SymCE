import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'n') and hasattr(witness, 'factors'):
            n = witness.n
            factors = witness.factors
        else:
            n, factors = witness
        h1 = isinstance(n, int) and n > 1
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'n') and hasattr(witness, 'factors'):
            n = witness.n
            factors = witness.factors
        else:
            n, factors = witness
            
        sigma_n = divisor_sigma(n)
        
        if isinstance(factors, dict):
            items = factors.items()
        else:
            items = factors
            
        prod = 1
        for p, k in items:
            if p == 1:
                prod = None
                break
            term = sympy.Rational(p**(k+1) - 1, p - 1)
            prod *= term
            
        if prod is None:
            neg_q = True
        else:
            neg_q = bool(sigma_n != prod)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "¬Q: sigma(n) is not equal to the product formula"
]

N_HYP = 1
NEG_Q_INDEX = 1
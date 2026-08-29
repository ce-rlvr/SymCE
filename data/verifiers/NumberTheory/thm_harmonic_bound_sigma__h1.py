import sympy
from sympy import Rational, divisor_sigma, harmonic

def conditions(witness) -> list[bool]:
    try:
        n_sym = sympy.S(witness)
        if not n_sym.is_integer:
            return [False]
        
        n = int(n_sym)
        if n == 0:
            return [False]
            
        lhs = divisor_sigma(abs(n))
        
        if n >= 1:
            rhs = n * harmonic(n)
        else:
            sum_val = sum(Rational(1, k) for k in range(1, n + 1))
            rhs = n * sum_val
            
        neg_q = not bool(lhs <= rhs)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: \\sigma(n) > n \\sum_{k=1}^n \\frac{1}{k}"
]

N_HYP = 0
NEG_Q_INDEX = 0
import sympy
from sympy import Symbol, cyclotomic_poly, divisors, expand

x = Symbol('x')

def conditions(witness) -> list[bool]:
    n = witness
    
    try:
        # H_1: n is an integer
        # The theorem implicitly requires n to be an integer for divisors(n) to make sense.
        h1 = isinstance(n, (int, sympy.Integer)) and not isinstance(n, bool)
    except Exception:
        h1 = False
        
    try:
        # Evaluate the conclusion: x^n - 1 == \prod_{d|n} \Phi_d(x)
        lhs = x**n - 1
        divs = divisors(n)
        rhs = 1
        for d in divs:
            rhs *= cyclotomic_poly(d, x)
        
        diff = expand(lhs - rhs)
        # neg_Q is True if the conclusion fails (i.e., the difference is not zero)
        neg_q = bool(diff != 0)
    except Exception:
        # If evaluation fails (e.g., divisors(0) raises an error), the formula is invalid,
        # meaning the conclusion fails at this witness.
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: x^n - 1 != \\prod_{d|n} \\Phi_d(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1
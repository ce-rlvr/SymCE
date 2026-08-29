import sympy
from sympy import Symbol, Poly, factor_list
from sympy.ntheory import isprime

# Top-level setup
x = Symbol('x')

def conditions(witness):
    try:
        f = Poly(witness, x)
        coeffs = f.all_coeffs()
        n = f.degree()
    except Exception:
        return [False, False, False, False]
        
    # H1: The degree n of f(x) is at least 1
    try:
        h1 = bool(n >= 1)
    except Exception:
        h1 = False
        
    # H2: a_0 = p or a_0 = -p for some prime number p
    try:
        a_0 = coeffs[-1]
        h2 = bool(a_0.is_integer is True and isprime(abs(int(a_0))))
    except Exception:
        h2 = False
        
    # H3: p > sum_{i=1}^{n-1} |a_i|
    try:
        if h2 and h1:
            p = abs(int(a_0))
            # coeffs is [a_n, a_{n-1}, ..., a_1, a_0]
            # coeffs[1:-1] gives [a_{n-1}, ..., a_1]
            sum_abs = sum(abs(c) for c in coeffs[1:-1])
            h3 = bool(p > sum_abs)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: f(x) is NOT irreducible over Q (i.e., it is reducible over Q)
    try:
        if h1:
            factors = factor_list(witness, x, domain='QQ')
            # Count the total number of non-constant factors (including multiplicities)
            num_factors = sum(exp for factor, exp in factors[1] if Poly(factor, x).degree() >= 1)
            neg_q = bool(num_factors > 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: The degree n of f(x) is at least 1",
    "H_2: a_0 = p or a_0 = -p for some prime number p",
    "H_3: p > sum_{i=1}^{n-1} |a_i|",
    "¬Q: f(x) is reducible over Q"
]

N_HYP = 3
NEG_Q_INDEX = 3
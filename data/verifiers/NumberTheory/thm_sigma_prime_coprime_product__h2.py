import sympy

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p does not divide m",
    r"¬Q: \sigma(p m) != (p+1)\sigma(m)"
]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        p, m = witness
    except Exception:
        return [False, False, False]
        
    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    # H_2: p does not divide m
    try:
        quotient = sympy.sympify(m) / sympy.sympify(p)
        is_int = quotient.is_integer
        if is_int is None:
            h2 = False
        else:
            h2 = not is_int
    except Exception:
        h2 = False
        
    # neg_Q: \sigma(p m) != (p+1)\sigma(m)
    try:
        try:
            # If m is not an integer (e.g. a rational number), divisor_sigma will raise an exception.
            # In that case, the conclusion is undefined and therefore fails.
            sigma_pm = sympy.ntheory.divisor_sigma(p * m)
            sigma_m = sympy.ntheory.divisor_sigma(m)
            conclusion = bool(sigma_pm == (p + 1) * sigma_m)
        except Exception:
            conclusion = False
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]
import sympy

CONDITION_LABELS = [
    "H_1: m/n is not a power of any prime number p",
    "¬Q: The resultant of the cyclotomic polynomials Phi_m(x) and Phi_n(x) is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            m = int(witness['m'])
            n = int(witness['n'])
        else:
            m = int(witness[0])
            n = int(witness[1])
        if m <= 0 or n <= 0:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: m/n is not a power of any prime number p
    try:
        if m % n == 0:
            val = m // n
            if val > 1:
                factors = sympy.factorint(val)
                is_prime_power = (len(factors) == 1)
            else:
                is_prime_power = False
        else:
            is_prime_power = False
            
        h1 = not is_prime_power
    except Exception:
        h1 = False
        
    # ¬Q: The resultant of the cyclotomic polynomials Phi_m(x) and Phi_n(x) is not exactly 1
    try:
        x = sympy.Symbol('x')
        poly_m = sympy.cyclotomic_poly(m, x)
        poly_n = sympy.cyclotomic_poly(n, x)
        res = sympy.resultant(poly_m, poly_n)
        neg_q = bool(res != 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]
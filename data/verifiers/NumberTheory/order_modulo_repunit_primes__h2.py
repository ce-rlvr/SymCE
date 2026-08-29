import sympy

def conditions(witness):
    try:
        n = int(witness)
        if n != witness:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: n is an integer strictly greater than 2
    try:
        h1 = bool(n > 2)
    except Exception:
        h1 = False
        
    # H_2: R_n is a prime number
    try:
        if n > 5000 or n < 1:
            h2 = False
        else:
            R_n = (10**n - 1) // 9
            h2 = bool(sympy.isprime(R_n))
    except Exception:
        h2 = False
        
    # neg_Q: The multiplicative order of 10 modulo R_n is not exactly n
    try:
        if n > 5000 or n < 1:
            neg_q = False
        else:
            R_n = (10**n - 1) // 9
            if R_n > 1:
                order = n
                # Since 10^n - 1 = 9 * R_n, 10^n == 1 mod R_n is always true.
                # Thus, the multiplicative order must divide n.
                for d in sympy.divisors(n):
                    if pow(10, d, R_n) == 1:
                        order = d
                        break
                neg_q = bool(order != n)
            else:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 2",
    "H_2: R_n is a prime number",
    "¬Q: The multiplicative order of 10 modulo R_n is not exactly n"
]

N_HYP = 2
NEG_Q_INDEX = 2
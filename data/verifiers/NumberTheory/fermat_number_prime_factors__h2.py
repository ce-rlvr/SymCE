import sympy

def conditions(witness):
    try:
        n, p = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: n is a positive integer
    try:
        if isinstance(n, (int, sympy.Integer)):
            h1 = int(n) > 0
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: p is a prime number
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False
        
    # H3: p divides F_n
    try:
        if h1 and h2:
            n_int = int(n)
            p_int = int(p)
            # F_n = 2^{2^n} + 1
            # p divides F_n iff 2^{2^n} == p - 1 mod p
            if p_int == 2:
                h3 = False
            else:
                # Use Fermat's Little Theorem to avoid computing huge exponents
                exp = pow(2, n_int, p_int - 1)
                val = pow(2, exp, p_int)
                h3 = (val == p_int - 1)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: p is NOT 1 mod 2^{n+1}
    try:
        if h1 and h2:
            n_int = int(n)
            p_int = int(p)
            # If 2^{n+1} > p, then p % 2^{n+1} == p. Since p is prime, p != 1.
            if n_int + 1 >= p_int.bit_length():
                neg_q = (p_int != 1)
            else:
                modulus = 2**(n_int + 1)
                neg_q = (p_int % modulus) != 1
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: p is a prime number",
    "H_3: p divides F_n",
    "¬Q: p is not congruent to 1 modulo 2^{n+1}"
]

N_HYP = 3
NEG_Q_INDEX = 3
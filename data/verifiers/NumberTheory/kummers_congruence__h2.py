import sympy

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p-1 does not divide n",
    "H_3: m == n (mod p-1)",
    "¬Q: B_m / m == B_n / n (mod p) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        p, m, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: p-1 does not divide n
    try:
        if p - 1 == 0:
            h2 = False
        else:
            h2 = (n % (p - 1)) != 0
    except Exception:
        h2 = False

    # H_3: m == n (mod p-1)
    try:
        if p - 1 == 0:
            h3 = False
        else:
            h3 = (m % (p - 1)) == (n % (p - 1))
    except Exception:
        h3 = False

    # ¬Q: B_m / m == B_n / n (mod p) fails
    try:
        if m <= 0 or n <= 0:
            neg_q = False
        else:
            Bm = sympy.bernoulli(m)
            Bn = sympy.bernoulli(n)
            term_m = sympy.Rational(Bm, m)
            term_n = sympy.Rational(Bn, n)
            diff = term_m - term_n
            
            # Congruence mod p for rationals:
            # a/b == 0 (mod p) iff p divides a and p does not divide b.
            # If p divides b, the expression is undefined mod p, so congruence fails.
            if diff.q % p == 0:
                congruent = False
            else:
                congruent = (diff.p % p == 0)
                
            neg_q = not congruent
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
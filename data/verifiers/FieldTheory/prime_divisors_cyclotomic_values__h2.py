import sympy
from sympy import isprime
from sympy.polys.specialpolys import cyclotomic_poly

x = sympy.Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
            a = witness.get('a')
        else:
            n, p, a = witness
    except Exception:
        return [False, False, False]

    # H_1: n >= 1 is an integer
    try:
        h1 = (int(n) == n) and (n >= 1)
    except Exception:
        h1 = False

    # H_2: p is a prime number dividing Phi_n(a)
    try:
        if not isprime(p):
            h2 = False
        else:
            poly = cyclotomic_poly(int(n), x)
            val = poly.subs(x, a)
            
            if isinstance(val, sympy.MatrixBase):
                h2 = all(entry % p == 0 for entry in val)
            else:
                h2 = (val % p == 0)
    except Exception:
        h2 = False

    # neg_Q: not (p divides n or p = 1 mod n)
    try:
        neg_q = not ((n % p == 0) or ((p - 1) % n == 0))
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: p is a prime number dividing Phi_n(a)",
    "¬Q: p does not divide n and p is not 1 mod n"
]

N_HYP = 2
NEG_Q_INDEX = 2
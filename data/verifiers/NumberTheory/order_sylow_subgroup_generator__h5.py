import sympy
import math

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    n, a, d_wit, p, k = None, None, None, None, None
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            p = witness.get('p')
            k = witness.get('k', 1)
            d_wit = witness.get('d')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 5:
                n, a, d_wit, p, k = witness
            elif len(witness) == 4:
                n, a, p, k = witness
            elif len(witness) == 3:
                n, a, p = witness
                k = 1
    except Exception:
        pass

    # H_1: n >= 2 is an integer
    try:
        if int(n) == n and n >= 2:
            h1 = True
            n = int(n)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: a is an integer coprime to n
    try:
        if int(a) == a and math.gcd(int(a), n) == 1:
            h2 = True
            a = int(a)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: d is the multiplicative order of a modulo n
    try:
        if h1 and h2:
            d_actual = sympy.n_order(a, n)
            if d_wit is not None:
                h3 = (int(d_wit) == d_actual)
            else:
                h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: p is a prime number
    try:
        if int(p) == p and sympy.isprime(int(p)):
            h4 = True
            p = int(p)
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: The multiplicative order of a^{d/p^k} modulo n is not exactly p^k
    try:
        if not (h1 and h2):
            neg_q = True
        else:
            d_actual = sympy.n_order(a, n)
            pk = p**k
            pk_int = int(pk)
            if pk_int != pk or pk_int <= 0:
                neg_q = True
            elif d_actual % pk_int != 0:
                neg_q = True
            else:
                exponent = d_actual // pk_int
                val = pow(a, exponent, n)
                order_val = sympy.n_order(val, n)
                neg_q = (order_val != pk_int)
    except Exception:
        neg_q = True

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "H_2: a is an integer coprime to n",
    "H_3: d is the multiplicative order of a modulo n",
    "H_4: p is a prime number",
    "¬Q: The multiplicative order of a^{d/p^k} modulo n is not exactly p^k"
]

N_HYP = 4
NEG_Q_INDEX = 4
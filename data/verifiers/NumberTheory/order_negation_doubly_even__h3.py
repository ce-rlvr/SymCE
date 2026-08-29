import sympy
import math

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            a = witness.get('a')
            d = witness.get('d')
        else:
            p, a, d = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is an odd prime number
    try:
        p_val = int(p)
        h1 = bool(sympy.isprime(p_val) and p_val % 2 != 0)
    except Exception:
        h1 = False

    # H_2: a is an integer coprime to p
    try:
        if not isinstance(a, (int, sympy.Integer)):
            h2 = False
        else:
            a_val = int(a)
            p_val = int(p)
            h2 = bool(math.gcd(a_val, p_val) == 1)
    except Exception:
        h2 = False

    # H_3: d is a multiple of 4
    try:
        if not isinstance(d, (int, sympy.Integer)):
            h3 = False
        else:
            d_val = int(d)
            h3 = bool(d_val % 4 == 0)
    except Exception:
        h3 = False

    # ¬Q: The multiplicative order of -a modulo p is not d
    try:
        a_val = int(a)
        p_val = int(p)
        d_val = int(d)
        
        if math.gcd(-a_val % p_val, p_val) == 1:
            try:
                order = sympy.n_order(-a_val % p_val, p_val)
                neg_q = bool(order != d_val)
            except Exception:
                neg_q = True
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: a is an integer coprime to p",
    "H_3: d is a multiple of 4",
    "¬Q: The multiplicative order of -a modulo p is not d"
]

N_HYP = 3
NEG_Q_INDEX = 3
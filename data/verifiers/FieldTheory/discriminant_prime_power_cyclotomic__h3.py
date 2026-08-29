import sympy
import math

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            k = witness.get('k')
            if 'D' in witness:
                val = witness['D']
            elif 'abs_disc' in witness:
                val = witness['abs_disc']
            elif 'K' in witness:
                val = witness['K']
            else:
                val = 1
        else:
            p = witness[0]
            k = witness[1]
            val = witness[2] if len(witness) > 2 else 1
            
        if hasattr(val, 'discriminant'):
            disc_attr = val.discriminant
            if callable(disc_attr):
                D = int(disc_attr())
            else:
                D = int(disc_attr)
        else:
            D = int(val)
    except Exception:
        return [False, False, False]

    # H1: p is a prime number
    try:
        p_int = int(p)
        h1 = (p_int == p) and sympy.isprime(p_int)
    except Exception:
        h1 = False

    # H2: k is a positive integer
    try:
        k_int = int(k)
        h2 = (k_int == k) and (k_int > 0)
    except Exception:
        h2 = False

    # neg_Q: The absolute value of the discriminant of K over Q is NOT equal to p^{p^{k-1}(pk-k-1)}
    try:
        p_val = int(p)
        k_val = int(k)
        exponent = (p_val**(k_val-1)) * (p_val*k_val - k_val - 1)
        if isinstance(exponent, (int, float)) and exponent > 1000000:
            neg_q = False
        else:
            expected_D = p_val**exponent
            neg_q = (abs(D) != expected_D)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: k is a positive integer",
    "¬Q: The absolute value of the discriminant of K over Q is not equal to p^{p^{k-1}(pk-k-1)}"
]

N_HYP = 2
NEG_Q_INDEX = 2
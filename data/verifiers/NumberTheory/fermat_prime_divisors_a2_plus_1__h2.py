import sympy
from sympy import eye, zeros, I

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            a = witness.get('a')
        else:
            p, a = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = sympy.isprime(p) and (p % 2 != 0)
    except Exception:
        h1 = False

    try:
        try:
            val = a**2 + 1
        except Exception:
            val = a**2 + eye(a.shape[0])
            
        if getattr(val, 'is_Matrix', False):
            h2 = all((elem % p) == 0 for elem in val)
        else:
            h2 = (val % p == 0)
    except Exception:
        h2 = False

    try:
        neg_q = (p % 4 != 1)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: p divides a^2 + 1",
    "¬Q: p is not 1 mod 4"
]

N_HYP = 2
NEG_Q_INDEX = 2
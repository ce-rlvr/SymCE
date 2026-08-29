import sympy
from sympy.ntheory import is_primitive_root, isprime, is_quad_residue

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = int(witness['a'])
            p = int(witness['p'])
        else:
            a, p = witness
            a = int(a)
            p = int(p)
    except Exception:
        return [False, False]

    # H_1: a is a primitive root modulo p
    try:
        h1 = bool(is_primitive_root(a, p))
    except Exception:
        h1 = False

    # ¬Q: a is a quadratic residue modulo p
    try:
        if p > 0:
            a_mod = a % p
            neg_q = False
            if p <= 100000:
                for x in range(p):
                    if (x * x) % p == a_mod:
                        neg_q = True
                        break
            else:
                if p % 2 != 0 and isprime(p):
                    neg_q = bool(is_quad_residue(a_mod, p))
                else:
                    neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is a primitive root modulo p",
    "¬Q: a is a quadratic residue modulo p"
]

N_HYP = 1
NEG_Q_INDEX = 1
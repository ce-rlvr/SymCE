import sympy
from sympy.ntheory import isprime
from sympy import oo
from sympy.abc import x, y, z

infinity = oo

def conditions(witness) -> list[bool]:
    # H1: K is a field of prime characteristic p > 0
    try:
        if isinstance(witness, dict):
            p = witness.get('char', witness.get('p'))
        else:
            p = getattr(witness, 'char', getattr(witness, 'p', None))
        p = int(p)
        h1_ok = isprime(p)
    except Exception:
        h1_ok = False

    # H2: E/K is purely inseparable
    try:
        if isinstance(witness, dict):
            is_pi = witness.get('purely_inseparable', witness.get('is_purely_inseparable'))
        else:
            is_pi = getattr(witness, 'purely_inseparable', getattr(witness, 'is_purely_inseparable', None))
        
        if is_pi is None:
            h2_ok = False
        else:
            h2_ok = bool(is_pi)
    except Exception:
        h2_ok = False

    # neg_Q: The degree of E over K is NOT equal to p^n for some integer n >= 0
    try:
        if isinstance(witness, dict):
            deg = witness.get('degree')
            p = witness.get('char', witness.get('p'))
        else:
            deg = getattr(witness, 'degree', None)
            p = getattr(witness, 'char', getattr(witness, 'p', None))
        
        if deg is None:
            neg_q_ok = False
        elif deg == oo or str(deg) == 'oo' or str(deg) == 'inf':
            neg_q_ok = True
        else:
            p = int(p)
            deg_int = int(deg)
            if p <= 1:
                neg_q_ok = False
            elif deg_int < 1:
                neg_q_ok = True
            else:
                temp = deg_int
                while temp % p == 0 and temp > 1:
                    temp //= p
                neg_q_ok = (temp != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: K is a field of prime characteristic p > 0", "H_2: E over K is purely inseparable", "¬Q: The degree of E over K is not equal to p^n for any integer n >= 0"]
N_HYP = 2
NEG_Q_INDEX = 2
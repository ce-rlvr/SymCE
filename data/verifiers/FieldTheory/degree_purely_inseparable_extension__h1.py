import sympy
from sympy import abc
import math

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_finite', False) and witness.get('is_purely_inseparable', False))
        else:
            h1 = bool(getattr(witness, 'is_finite', False) and getattr(witness, 'is_purely_inseparable', False))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            deg = witness.get('degree', 1)
            p = witness.get('p', 0)
        else:
            deg = getattr(witness, 'degree', 1)
            p = getattr(witness, 'p', 0)
        
        if p == 0:
            is_pow = (deg == 1)
        elif p == 1:
            is_pow = (deg == 1)
        else:
            temp = deg
            while temp > 0 and temp % p == 0:
                temp //= p
            is_pow = (temp == 1)
        neg_q = not is_pow
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a finite purely inseparable field extension",
    "¬Q: The degree of the extension E over F is not a power of p"
]

N_HYP = 1
NEG_Q_INDEX = 1
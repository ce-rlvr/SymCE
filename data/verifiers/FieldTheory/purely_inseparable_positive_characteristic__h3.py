import sympy
from sympy import QQ, ZZ, RR, CC, GF

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: E/F is a field extension",
    "H_2: The extension E/F is purely inseparable",
    "¬Q: The characteristic of F is not a prime p > 0"
]

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            E, F = witness
        else:
            E = F = witness
    except Exception:
        return [False, False, False]

    # H_1: E/F is a field extension
    try:
        h1 = False
        if getattr(E, 'is_Field', False) and getattr(F, 'is_Field', False):
            if E == F:
                h1 = True
            elif hasattr(E, 'domain') and E.domain == F:
                h1 = True
    except Exception:
        h1 = False

    # H_2: The extension E/F is purely inseparable
    try:
        h2 = False
        if h1:
            if E == F:
                h2 = True
            else:
                char = F.characteristic()
                if char > 0:
                    if hasattr(E, 'mod'):
                        if E.mod.diff().is_zero:
                            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The characteristic of F is not a prime p > 0
    try:
        char = F.characteristic()
        neg_q = (char == 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
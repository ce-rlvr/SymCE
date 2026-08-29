import sympy
from sympy.ntheory import legendre_symbol

def conditions(witness):
    try:
        if isinstance(witness, bool) or not isinstance(witness, (int, sympy.Integer)):
            h1 = False
        else:
            h1 = (witness != 5)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, bool) or not isinstance(witness, (int, sympy.Integer)):
            q = False
        else:
            mod5 = witness % 5
            if mod5 in (1, 4):
                try:
                    q = (legendre_symbol(5, witness) == 1)
                except ValueError:
                    q = False
            elif mod5 in (2, 3):
                try:
                    q = (legendre_symbol(5, witness) == -1)
                except ValueError:
                    q = False
            else:
                q = True
    except Exception:
        q = False

    neg_q = not q

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p != 5",
    "¬Q: The Legendre symbol (5/p) does not equal 1 for p=1,4 mod 5, or does not equal -1 for p=2,3 mod 5"
]

N_HYP = 1
NEG_Q_INDEX = 1
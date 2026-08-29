import sympy
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        # Parse witness
        if isinstance(witness, dict):
            f = witness.get('f', x**5 - 3)
            d = witness.get('E_degree', witness.get('d', witness.get('degree', witness.get('E', None))))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                f, d = witness
            elif len(witness) >= 1:
                f = x**5 - 3
                d = witness[0]
            else:
                f = x**5 - 3
                d = None
        else:
            f = x**5 - 3
            d = witness

        # H_1: f(x) = x^5 - 3
        try:
            h1 = (sympy.simplify(f - (x**5 - 3)) == 0)
        except Exception:
            h1 = False

        # ¬Q: The degree of the extension E over Q is not 20
        try:
            d_val = int(d)
            neg_q = (d_val != 20 and d_val > 0)
        except Exception:
            neg_q = False

        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = ["H_1: f(x) = x^5 - 3", "¬Q: The degree of the extension E over Q is not 20"]
N_HYP = 1
NEG_Q_INDEX = 1
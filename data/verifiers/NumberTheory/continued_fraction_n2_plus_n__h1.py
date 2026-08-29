import sympy
from sympy import sqrt, Rational
from sympy.ntheory import continued_fraction_periodic

def conditions(witness) -> list[bool]:
    try:
        n = Rational(witness)
        h1 = bool(n >= 1)
    except Exception:
        h1 = False

    try:
        n = Rational(witness)
        val = sqrt(n**2 + n)
        cf = continued_fraction_periodic(val)
        
        if isinstance(cf, list):
            q_ok = False
        else:
            non_per, per = cf
            if not n.is_integer:
                q_ok = False
            else:
                if n == 1:
                    q_ok = (list(non_per) == [1] and list(per) == [2])
                else:
                    q_ok = (list(non_per) == [n] and list(per) == [2, 2*n])
    except Exception:
        q_ok = False

    neg_q = not q_ok

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1",
    "¬Q: CF expansion of sqrt(n**2+n) is not purely periodic with period 2, 2n"
]

N_HYP = 1
NEG_Q_INDEX = 1
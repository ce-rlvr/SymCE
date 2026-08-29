import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y, z
from sympy.ntheory import factorint, isprime

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: The group of units of the polynomial ring over R is not equal to the group of units of R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        h1 = False
        if isinstance(witness, (int, sympy.Integer)):
            h1 = isprime(abs(int(witness)))
        elif hasattr(witness, 'is_UFD'):
            h1 = bool(witness.is_UFD)
    except Exception:
        h1 = False

    try:
        neg_q = False
        if isinstance(witness, (int, sympy.Integer)):
            val = abs(int(witness))
            if val in (0, 1):
                neg_q = False
            else:
                factors = factorint(val)
                neg_q = any(v > 1 for v in factors.values())
        else:
            if hasattr(witness, 'is_Domain') and witness.is_Domain:
                neg_q = False
            elif hasattr(witness, 'has_nilpotent'):
                neg_q = bool(witness.has_nilpotent())
    except Exception:
        neg_q = False

    return [h1, neg_q]
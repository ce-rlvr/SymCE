import sympy
import sympy.abc
from sympy import ZZ, QQ, RR, CC

# Top-level setup
Z = ZZ
Q = QQ

def conditions(witness) -> list[bool]:
    try:
        # Witness can be a tuple (R, x) or just x (defaulting to R = ZZ)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, x = witness
        else:
            R, x = ZZ, witness
            
        # H_1: R is an integral domain
        try:
            if R in (ZZ, QQ, RR, CC):
                h1 = True
            elif hasattr(R, 'is_Domain') and R.is_Domain:
                h1 = True
            else:
                h1 = False
        except Exception:
            h1 = False
            
        # ¬Q: The annihilator ideal of x in R is not the zero ideal {0}
        # In an integral domain, Ann(x) != {0} if and only if x == 0.
        try:
            if hasattr(R, 'zero') and x == R.zero:
                neg_q = True
            elif hasattr(x, 'is_zero') and x.is_zero is not None:
                neg_q = bool(x.is_zero)
            else:
                neg_q = bool(x == 0)
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The annihilator ideal of x in R is not the zero ideal {0}"
]

N_HYP = 1
NEG_Q_INDEX = 1
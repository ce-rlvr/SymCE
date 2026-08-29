import sympy
import sympy.ntheory
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    neg_q = False
    try:
        if isinstance(witness, (int, Integer)):
            n = abs(int(witness))
            if n == 0:
                # n = 0 represents Z/0Z = Z, which is an integral domain, so Spec(Z) is connected.
                neg_q = False
            elif n == 1:
                # n = 1 represents Z/1Z = 0, the zero ring. Spec(0) is empty, hence disconnected.
                neg_q = True
            else:
                # n > 1 represents Z/nZ. Spec(Z/nZ) is connected iff n is a prime power.
                factors = sympy.ntheory.factorint(n)
                neg_q = len(factors) > 1
        elif isinstance(witness, (tuple, list)):
            # A tuple or list represents a product of rings.
            # A product of more than one non-trivial ring has non-trivial idempotents.
            neg_q = len(witness) > 1
    except Exception:
        pass
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: Spec(R) is not connected"
]

N_HYP = 0
NEG_Q_INDEX = 0
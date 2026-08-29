import sympy
import sympy.ntheory
from sympy.polys.domains import ZZ, QQ, FF

# Standard rings represented as integers n for Z/nZ (0 means Z)
Z = 0
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7

# Standard SymPy finite fields
FF2 = FF(2)
FF3 = FF(3)
FF5 = FF(5)
FF7 = FF(7)

def conditions(witness) -> list[bool]:
    # H_1: R is an integral domain
    try:
        if isinstance(witness, (int, sympy.Integer)):
            w = int(witness)
            if w == 0:
                h1 = True
            elif w > 0:
                h1 = sympy.ntheory.isprime(w)
            else:
                h1 = False
        else:
            # In SymPy, all implemented polynomial domains are integral domains.
            # We duck-type by checking for the characteristic attribute.
            h1 = hasattr(witness, 'characteristic') or hasattr(witness, 'char')
    except Exception:
        h1 = False

    # neg_Q: The characteristic of R is NOT zero
    try:
        if isinstance(witness, (int, sympy.Integer)):
            char = int(witness)
        else:
            if hasattr(witness, 'characteristic'):
                c = witness.characteristic
                char = c() if callable(c) else c
            elif hasattr(witness, 'char'):
                c = witness.char
                char = c() if callable(c) else c
            else:
                char = 0
        neg_q = (char != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The characteristic of R is not zero"
]

N_HYP = 1
NEG_Q_INDEX = 1
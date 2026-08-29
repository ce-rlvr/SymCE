import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.ntheory import isprime

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The polynomial ring over R is not an integral domain"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    if isinstance(witness, str):
        w_str = witness.upper().replace(' ', '')
        if w_str.startswith('Z/') and w_str.endswith('Z'):
            try:
                witness = int(w_str[2:-1])
            except ValueError:
                pass
        elif w_str.startswith('Z'):
            try:
                witness = int(w_str[1:])
            except ValueError:
                pass

    h1 = False
    try:
        if isinstance(witness, int):
            h1 = witness >= 2
        elif witness in [ZZ, QQ]:
            h1 = True
        elif hasattr(witness, 'is_Ring') and witness.is_Ring:
            h1 = True
    except Exception:
        h1 = False

    neg_q = False
    try:
        if isinstance(witness, int):
            neg_q = not isprime(witness)
        elif witness in [ZZ, QQ]:
            neg_q = False
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            neg_q = False
        elif hasattr(witness, 'is_PID') and witness.is_PID:
            neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]
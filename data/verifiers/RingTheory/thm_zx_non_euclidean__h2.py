import sympy
from sympy import ZZ, QQ, Symbol

# Top-level setup
x = Symbol('x')
ZZ_x = ZZ[x]
QQ_x = QQ[x]

def conditions(witness):
    try:
        # H_1: Z is the ring of integers
        # This is a background fact. We just verify the witness is a valid ring/domain.
        h1_ok = hasattr(witness, 'is_Ring') or hasattr(witness, 'is_Field') or witness in (ZZ, QQ, ZZ_x, QQ_x)
        h1_ok = bool(h1_ok)
    except Exception:
        h1_ok = False

    try:
        # neg_Q: R is a Euclidean domain
        neg_q = False
        if witness == ZZ:
            neg_q = True
        elif getattr(witness, 'is_Field', False):
            neg_q = True
        elif hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
            # A polynomial ring over a field in one variable is a Euclidean domain
            if getattr(witness.domain, 'is_Field', False) and len(witness.symbols) == 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: Z is the ring of integers",
    "¬Q: R is a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1
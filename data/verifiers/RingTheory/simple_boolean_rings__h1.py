import sympy
from sympy.polys.domains import QQ, ZZ, RR, CC, GF

# Top-level setup: named object bindings that the witness expression may reference.
Z2 = GF(2)
Z3 = GF(3)
Z5 = GF(5)
Z7 = GF(7)

def conditions(witness) -> list[bool]:
    # H_1: R is a simple ring
    # A commutative ring is simple iff it is a field.
    # We support witnesses provided as integers (representing Z_n) or SymPy domains.
    try:
        if isinstance(witness, (int, sympy.Integer)):
            h1 = sympy.isprime(int(witness))
        elif hasattr(witness, 'is_Field'):
            h1 = bool(witness.is_Field)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: R is not isomorphic to Z_2
    try:
        if isinstance(witness, (int, sympy.Integer)):
            is_z2 = (int(witness) == 2)
        elif witness == GF(2):
            is_z2 = True
        elif hasattr(witness, 'order') and callable(witness.order):
            is_z2 = (int(witness.order()) == 2)
        elif hasattr(witness, 'order'):
            is_z2 = (int(witness.order) == 2)
        elif hasattr(witness, 'mod'):
            is_z2 = (int(witness.mod) == 2)
        else:
            is_z2 = False
        neg_q = not is_z2
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a simple ring",
    "¬Q: R is not isomorphic to Z_2"
]

N_HYP = 1
NEG_Q_INDEX = 1
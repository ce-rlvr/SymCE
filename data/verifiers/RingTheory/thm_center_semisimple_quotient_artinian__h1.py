import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    try:
        # H_1: J(R) is the Jacobson radical of R
        # We accept SymPy domains (like ZZ, QQ) as rings.
        h1 = hasattr(witness, 'is_Field') and hasattr(witness, 'get_ring')
    except Exception:
        h1 = False

    try:
        # ¬Q: The center of R/J(R) is not isomorphic to a finite direct product of fields
        # For ZZ, J(ZZ) = 0, R/J(R) = ZZ. Center of ZZ is ZZ.
        # ZZ is not a finite direct product of fields.
        if h1:
            neg_q = not witness.is_Field
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: J(R) is the Jacobson radical of R",
    "¬Q: The center of R/J(R) is not isomorphic to a finite direct product of fields"
]

N_HYP = 1
NEG_Q_INDEX = 1
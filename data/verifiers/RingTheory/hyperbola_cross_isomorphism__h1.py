import sympy
from sympy import GF, QQ, ZZ

# Top-level setup
# The witness is expected to be a field (e.g., GF(2), QQ) or an integer representing a prime field characteristic.

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    """
    # H_1: F is a field
    h1 = False
    try:
        if isinstance(witness, (int, sympy.Integer)):
            h1 = sympy.isprime(int(witness))
        elif hasattr(witness, 'is_Field'):
            h1 = bool(witness.is_Field)
        elif witness == QQ:
            h1 = True
    except Exception:
        pass

    # ¬Q: R/(x^2 - y^2) is not isomorphic to S/(uv)
    # This is true if and only if the characteristic of F is 2 (for fields),
    # because in characteristic 2, x^2 - y^2 = (x+y)^2 has a repeated factor,
    # making R/I non-reduced, whereas S/(uv) is always reduced.
    neg_q = False
    try:
        char = None
        if isinstance(witness, (int, sympy.Integer)):
            char = int(witness)
        elif hasattr(witness, 'characteristic'):
            char = witness.characteristic()
        elif witness == QQ:
            char = 0
            
        if char == 2:
            neg_q = True
        elif witness == ZZ:
            # Z[x,y]/(x^2-y^2) is also not isomorphic to Z[u,v]/(uv)
            neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: R/(x^2 - y^2) is not isomorphic to S/(uv)"
]

N_HYP = 1
NEG_Q_INDEX = 1
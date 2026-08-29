import sympy
from sympy.abc import x, y, z

# Standard ring and field domains
ZZ = sympy.ZZ
QQ = sympy.QQ
QQ_x = QQ[x]
ZZ_x = ZZ[x]

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, a, b).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, a, b = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: R is a Euclidean domain
    try:
        # In SymPy, Euclidean domains (like ZZ, QQ[x]) are represented as PIDs.
        h1 = hasattr(R, 'is_PID') and R.is_PID
    except Exception:
        h1 = False

    # neg_Q: There does NOT exist a least common multiple of a and b in R
    try:
        # Divisibility in a ring R is a relation on R x R.
        # If a or b is not an element of R, they have no multiples in R,
        # hence no common multiples, and therefore no least common multiple in R.
        # If they are both in R, since R is a Euclidean domain, their LCM always exists.
        if a in R and b in R:
            neg_q = False
        else:
            neg_q = True
    except Exception:
        # If membership checking fails, we assume they don't have an LCM in R.
        neg_q = True

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: There does not exist a least common multiple of a and b in R"
]

N_HYP = 1
NEG_Q_INDEX = 1
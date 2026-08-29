import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup: standard rings that might be used as witnesses
Z_x = ZZ[x]
Q_x = QQ[x]
Q_x_y = QQ[x, y]
Z_x_y = ZZ[x, y]

def krull_dimension(R):
    """
    Helper function to compute the Krull dimension of standard SymPy domains.
    """
    if getattr(R, 'is_Field', False):
        return 0
    if R == ZZ:
        return 1
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        return krull_dimension(R.domain) + len(R.symbols)
    raise ValueError(f"Cannot determine Krull dimension for {R}")

def conditions(witness) -> list[bool]:
    # H_1: R is not a field
    try:
        h1 = not bool(witness.is_Field)
    except Exception:
        h1 = False

    # ¬Q: The Krull dimension of R is not exactly 1
    try:
        dim = krull_dimension(witness)
        neg_q = (dim != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is not a field",
    "¬Q: The Krull dimension of R is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
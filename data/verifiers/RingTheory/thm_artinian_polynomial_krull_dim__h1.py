import sympy
from sympy import QQ, ZZ

# Top-level setup
Z2 = sympy.GF(2)
Z3 = sympy.GF(3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the conjecture:
    "If R is an Artinian ring, then the Krull dimension of the polynomial ring over R is exactly 1."
    """
    # H_1: R is an Artinian ring
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_artinian', False))
        elif isinstance(witness, tuple) and len(witness) >= 1:
            h1 = bool(witness[0])
        elif hasattr(witness, 'is_artinian'):
            h1 = bool(witness.is_artinian)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: The Krull dimension of the polynomial ring over R is NOT exactly 1
    try:
        if isinstance(witness, dict):
            dim = witness.get('krull_dimension_poly_ring', None)
        elif isinstance(witness, tuple) and len(witness) >= 2:
            dim = witness[1]
        elif hasattr(witness, 'krull_dimension_poly_ring'):
            dim = witness.krull_dimension_poly_ring
        else:
            dim = None
            
        if dim is None:
            neg_q = False
        else:
            neg_q = (dim != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an Artinian ring",
    "not Q: The Krull dimension of the polynomial ring over R is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
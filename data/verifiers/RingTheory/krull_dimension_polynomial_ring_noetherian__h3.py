import math
import sympy

def conditions(witness) -> list[bool]:
    # H_1: R is a commutative ring
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_commutative", False))
        else:
            h1 = bool(getattr(witness, "is_commutative", False))
    except Exception:
        h1 = False

    # H_2: R is Noetherian
    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get("is_noetherian", False))
        else:
            h2 = bool(getattr(witness, "is_noetherian", False))
    except Exception:
        h2 = False

    # not Q: The Krull dimension of the polynomial ring is not exactly d + 1
    try:
        if isinstance(witness, dict):
            d = witness.get("krull_dimension", None)
            dim_Rx = witness.get("poly_ring_krull_dimension", None)
        else:
            d = getattr(witness, "krull_dimension", None)
            dim_Rx = getattr(witness, "poly_ring_krull_dimension", None)
            
        if d is None or dim_Rx is None:
            neg_q = False
        else:
            d_inf = d == float('inf') or d == sympy.oo or str(d).lower() in ['inf', 'infinity']
            dim_Rx_inf = dim_Rx == float('inf') or dim_Rx == sympy.oo or str(dim_Rx).lower() in ['inf', 'infinity']
            
            if d_inf or dim_Rx_inf:
                q = False
            else:
                q = (dim_Rx == d + 1)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is Noetherian",
    "not Q: The Krull dimension of the polynomial ring is not exactly d + 1"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy

def conditions(witness):
    try:
        if hasattr(witness, 'is_integral_domain'):
            val = witness.is_integral_domain
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_domain'):
            val = witness.is_domain
            h1 = bool(val() if callable(val) else val)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'jacobson_radical_polynomial_ring_is_zero'):
            val = witness.jacobson_radical_polynomial_ring_is_zero
            q = bool(val() if callable(val) else val)
        else:
            q = True
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The Jacobson radical of the polynomial ring is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1
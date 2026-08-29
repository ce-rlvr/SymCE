import sympy
from sympy import QQ, RR, CC, ZZ

# Top-level setup
# We provide standard fields and rings for the witness expression to reference.
# QQ, RR, CC, ZZ are already imported and available in the namespace.

def conditions(witness) -> list[bool]:
    try:
        # The hypothesis states F^x is the multiplicative group of units of F.
        # This implicitly requires the witness F to be a field.
        h1 = bool(witness.is_Field)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # The conclusion is that F^x is a cyclic group.
            # For a field F, its multiplicative group F^x is cyclic if and only if F is a finite field.
            # Therefore, the conclusion fails (neg_q is True) iff F is an infinite field.
            is_finite = False
            if hasattr(witness, 'order'):
                is_finite = True
            elif hasattr(witness, 'is_finite') and witness.is_finite:
                is_finite = True
            elif witness.__class__.__name__ in ['FiniteField', 'GaloisField']:
                is_finite = True
            
            neg_q = not is_finite
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F^x is the multiplicative group of units of F",
    "¬Q: F^x is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1
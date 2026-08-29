import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def is_artinian(ring):
    """
    Helper function to determine if a SymPy domain is an Artinian ring.
    Fields and finite rings are Artinian. ZZ and polynomial rings are not.
    """
    try:
        if not getattr(ring, 'is_Ring', False):
            return False
        if getattr(ring, 'is_Field', False):
            return True
        if ring == ZZ:
            return False
        if hasattr(ring, 'gens'):  # Polynomial rings are not Artinian
            return False
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        # Witness should be a tuple of two rings (R1, R2)
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        R1, R2 = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = is_artinian(R1)
    except Exception:
        h1 = False
        
    try:
        # The conclusion is that the direct product R1 x R2 is an Artinian ring.
        # A direct product of rings is Artinian if and only if both rings are Artinian.
        # The conclusion fails (neg_Q is True) if R1 x R2 is NOT Artinian.
        # We also require R2 to be a valid ring for the product to make sense.
        if not getattr(R2, 'is_Ring', False):
            neg_q = False
        else:
            neg_q = not (is_artinian(R1) and is_artinian(R2))
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R_1 is an Artinian ring",
    "¬Q: R_1 x R_2 is not an Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1
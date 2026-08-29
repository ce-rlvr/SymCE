import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    try:
        # The witness must be a SymPy domain (ring/field)
        if not hasattr(witness, 'is_Field'):
            return [False]
            
        # Check if the ring is right Artinian.
        # Being right Artinian is a Morita invariant.
        # Thus, R is Morita equivalent to a basic right Artinian ring
        # if and only if R itself is right Artinian.
        is_artinian = False
        if witness.is_Field:
            is_artinian = True
        elif witness == ZZ:
            is_artinian = False
        elif hasattr(witness, 'is_PolynomialRing') and witness.is_PolynomialRing:
            is_artinian = False
        else:
            # For other typical SymPy domains (which are mostly infinite and not fields),
            # they are not Artinian.
            is_artinian = False
            
        neg_q = not is_artinian
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: R is not Morita equivalent to a basic right Artinian ring"
]

N_HYP = 0
NEG_Q_INDEX = 0
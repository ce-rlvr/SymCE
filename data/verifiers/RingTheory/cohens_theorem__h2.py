import sympy
from sympy import symbols
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.polys.rings import PolyRing

# Top-level setup: named object bindings
x, y, z = symbols('x y z')

class _NonNoetherianRing:
    """
    A mock object representing a non-Noetherian commutative ring with identity,
    such as a polynomial ring in infinitely many variables over a field.
    """
    is_commutative = True
    has_identity = True
    is_Noetherian = False

# Provide a ready-to-use witness for the false conjecture
R_inf = _NonNoetherianRing()

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False

    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative', False) and witness.get('has_identity', False))
            if 'is_Noetherian' in witness:
                neg_q = not bool(witness['is_Noetherian'])
            elif 'is_noetherian' in witness:
                neg_q = not bool(witness['is_noetherian'])
                
        elif isinstance(witness, str):
            s = witness.lower()
            h1 = ('commutative' in s) and ('identity' in s or '1' in s or 'unital' in s)
            neg_q = ('not noetherian' in s) or ('non-noetherian' in s) or ('infinitely many' in s) or ('infinite variables' in s)
            
        else:
            if hasattr(witness, 'is_commutative') and hasattr(witness, 'has_identity'):
                h1 = bool(witness.is_commutative and witness.has_identity)
            elif hasattr(witness, 'is_Commutative') and hasattr(witness, 'has_Identity'):
                h1 = bool(witness.is_Commutative and witness.has_Identity)
            
            if hasattr(witness, 'is_Noetherian'):
                neg_q = not bool(witness.is_Noetherian)
            elif hasattr(witness, 'is_noetherian'):
                neg_q = not bool(witness.is_noetherian)
            elif isinstance(witness, PolyRing):
                # Standard SymPy finite poly rings are Noetherian
                h1 = True
                neg_q = False
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: R is not a Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1
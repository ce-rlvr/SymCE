import sympy
from sympy import CC, QQ, ZZ, RR
from sympy.polys.domains import FF
import math

# Define a representation for the trivial ring, which is the standard counterexample
# for this conjecture (it is algebraically closed, finite, and not a field).
class TrivialRing:
    @property
    def is_algebraically_closed(self):
        return True
    
    @property
    def is_finite(self):
        return True
        
    @property
    def is_field(self):
        return False
        
    def __str__(self):
        return "trivial_ring"

trivial_ring = TrivialRing()
TrivialRingObj = trivial_ring
Z1 = trivial_ring
trivial = trivial_ring

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If K is algebraically closed, then the field K has infinitely many elements."
    """
    # H1: K is algebraically closed
    try:
        if hasattr(witness, 'is_algebraically_closed'):
            h1 = bool(witness.is_algebraically_closed)
        elif witness == sympy.CC or str(witness) == 'CC':
            h1 = True
        elif str(witness).lower() in ["trivial", "trivial_ring", "trivial ring", "{0}", "0", "1"]:
            h1 = True
        elif witness in [0, 1]:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: The conclusion "The field K has infinitely many elements" FAILS.
    # This means K is either not a field, or it does not have infinitely many elements.
    try:
        # Check if it's a field
        if hasattr(witness, 'is_field'):
            is_f = bool(witness.is_field)
        elif hasattr(witness, 'is_Field'):
            is_f = bool(witness.is_Field)
        elif witness in [sympy.CC, sympy.QQ, sympy.RR] or str(witness) in ['CC', 'QQ', 'RR']:
            is_f = True
        elif witness == sympy.ZZ or str(witness) == 'ZZ':
            is_f = False
        elif str(witness).lower() in ["trivial", "trivial_ring", "trivial ring", "{0}", "0", "1"]:
            is_f = False
        elif witness in [0, 1]:
            is_f = False
        else:
            is_f = True  # Default to True so we don't trivially pass neg_Q for unknown fields

        # Check if it has infinitely many elements
        if hasattr(witness, 'is_finite'):
            inf = not witness.is_finite
        elif witness in [sympy.CC, sympy.QQ, sympy.ZZ, sympy.RR] or str(witness) in ['CC', 'QQ', 'ZZ', 'RR']:
            inf = True
        elif str(witness).lower() in ["trivial", "trivial_ring", "trivial ring", "{0}", "0", "1"]:
            inf = False
        elif witness in [0, 1]:
            inf = False
        elif hasattr(witness, 'order'):
            try:
                inf = (witness.order == sympy.oo or math.isinf(float(witness.order)))
            except Exception:
                inf = False
        else:
            inf = False
            
        neg_q = not (is_f and inf)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is algebraically closed",
    "¬Q: K is not a field or K does not have infinitely many elements"
]

N_HYP = 1
NEG_Q_INDEX = 1
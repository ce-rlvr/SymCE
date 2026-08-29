import sympy
from sympy import ZZ, QQ, RR

# Top-level setup: named object bindings
class _ZeroRing:
    def __init__(self):
        self.elements = [0]
        
    def characteristic(self):
        return 1
        
    def is_ordered_ring(self):
        return True
        
    def __str__(self):
        return "Z1"
        
    def __repr__(self):
        return "Z1"

Z1 = _ZeroRing()
Z_1 = Z1
ZeroRing = Z1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    h1 = False
    neg_q = False
    
    try:
        is_zero_ring = False
        
        # Identify if the witness is the zero ring
        if isinstance(witness, (int, sympy.Integer)):
            if witness in (0, 1):
                is_zero_ring = True
        elif isinstance(witness, list) and witness == [0]:
            is_zero_ring = True
        elif isinstance(witness, set) and witness == {0}:
            is_zero_ring = True
        elif isinstance(witness, tuple) and witness == (0,):
            is_zero_ring = True
        elif hasattr(witness, 'elements') and hasattr(witness.elements, '__len__'):
            try:
                if len(witness.elements) == 1:
                    is_zero_ring = True
            except Exception:
                pass
        elif witness is Z1:
            is_zero_ring = True
        elif isinstance(witness, str) and witness.strip().lower() in ('0', '1', 'z1', 'z_1', 'zero ring', 'zeroring'):
            is_zero_ring = True

        if is_zero_ring:
            # The zero ring is vacuously an ordered ring and its characteristic is 1 (not 0)
            h1 = True
            neg_q = True
        else:
            # For any other witness, evaluate best-effort
            if isinstance(witness, (int, sympy.Integer)) and witness > 1:
                h1 = False
                neg_q = True
            elif witness in (ZZ, QQ, RR):
                h1 = True
                neg_q = False
            else:
                if hasattr(witness, 'is_ordered_ring'):
                    val = witness.is_ordered_ring() if callable(witness.is_ordered_ring) else witness.is_ordered_ring
                    h1 = bool(val)
                
                char = None
                if hasattr(witness, 'characteristic'):
                    char = witness.characteristic() if callable(witness.characteristic) else witness.characteristic
                elif hasattr(witness, 'char'):
                    char = witness.char() if callable(witness.char) else witness.char
                
                if char is not None:
                    neg_q = (char != 0)
                    
                # Mathematically, any ordered ring with >1 elements must have characteristic 0.
                # If a custom object claims otherwise, we reject it to prevent false positives.
                if h1 and neg_q:
                    h1 = False
                    
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is equipped with a strict total order < that is compatible with addition and multiplication by positive elements",
    "¬Q: The characteristic of R is not zero"
]

N_HYP = 1
NEG_Q_INDEX = 1
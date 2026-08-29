import sympy
from sympy import QQ, RR, CC, ZZ

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    
    The conjecture states:
    H1: F is a field
    H2: \overline{F} is the algebraic closure of F
    Q: \overline{F} cannot be equipped with a strict total order that makes it an ordered field.
    
    Since \overline{F} is algebraically closed, the equation x^2 + 1 = 0 always has a root in \overline{F}.
    In any ordered field, squares must be non-negative, so -1 cannot be a square.
    Therefore, NO algebraically closed field can EVER be ordered.
    This means the conclusion Q is unconditionally TRUE for all fields F.
    Consequently, the negated conclusion (¬Q) is unconditionally FALSE.
    """
    try:
        # Handle cases where witness might be passed as a tuple (F, F_bar) or just F
        if isinstance(witness, tuple) and len(witness) == 2:
            F = witness[0]
        else:
            F = witness
            
        # Check H1: F is a field
        h1 = False
        if F in [QQ, RR, CC]:
            h1 = True
        elif hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif hasattr(F, 'is_field') and F.is_field:
            h1 = True
        elif hasattr(F, 'has_characteristic'):
            h1 = True
            
        # Check H2: \overline{F} is the algebraic closure of F
        # This is definitional. If F is a field, it has an algebraic closure.
        h2 = h1
        
        # Check ¬Q: \overline{F} CAN be equipped with a strict total order
        # As explained above, this is mathematically impossible.
        neg_q = False
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: \overline{F} is the algebraic closure of F",
    "¬Q: \overline{F} can be equipped with a strict total order that makes it an ordered field"
]

N_HYP = 2
NEG_Q_INDEX = 2
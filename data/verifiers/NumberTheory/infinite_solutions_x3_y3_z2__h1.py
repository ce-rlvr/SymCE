import sympy
from sympy import symbols

# Top-level setup
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims "The set S is infinite" without any hypotheses defining S.
    A valid counterexample is any finite set.
    """
    try:
        neg_q = False
        # Check if the witness is a SymPy set with the is_finite property
        if hasattr(witness, 'is_finite') and witness.is_finite is not None:
            neg_q = bool(witness.is_finite)
        # Check if the witness is a finite group/ring with an order
        elif hasattr(witness, 'order'):
            try:
                ord_val = witness.order()
                neg_q = (ord_val < float('inf'))
            except Exception:
                pass
        # Check if the witness is a standard Python finite collection
        elif isinstance(witness, (list, set, tuple, frozenset, dict)):
            neg_q = True
    except Exception:
        neg_q = False
        
    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: The set S is finite"
]

N_HYP = 0
NEG_Q_INDEX = 0
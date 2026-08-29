import sympy
from sympy import S, Interval, Union, Intersection

# Top-level setup
Reals = S.Reals
Rationals = S.Rationals
Integers = S.Integers
Naturals = S.Naturals
EmptySet = S.EmptySet

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the conjecture:
    "The connected components of X form a partition of the space X"
    
    The only topological space where the connected components do not form a valid 
    partition (under the standard definition that a partition cannot be empty or 
    contain empty sets) is the empty space.
    """
    try:
        if witness == S.EmptySet:
            neg_q = True
        elif isinstance(witness, (list, set, tuple)) and len(witness) == 0:
            neg_q = True
        elif hasattr(witness, 'is_empty') and witness.is_empty:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: The connected components of X do not form a partition of X (e.g., X is empty)"
]

N_HYP = 0
NEG_Q_INDEX = 0
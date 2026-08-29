import sympy
from sympy import Interval, oo, FiniteSet

N_HYP = 0
NEG_Q_INDEX = 0

CONDITION_LABELS = [
    "¬Q: The set A is not topologically dense in the interval [1, \infty)"
]

def conditions(witness):
    try:
        if isinstance(witness, (list, set, tuple)):
            witness = FiniteSet(*witness)
        elif isinstance(witness, (int, float)):
            witness = FiniteSet(witness)
            
        is_dense = Interval(1, oo).is_subset(witness.closure)
        neg_q = not bool(is_dense)
    except Exception:
        neg_q = False
        
    return [neg_q]
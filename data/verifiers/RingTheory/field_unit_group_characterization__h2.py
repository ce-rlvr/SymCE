import sympy
import math
import itertools
import functools

# Top-level setup
Z1 = 1
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture:
    "A commutative ring R is a field if and only if the group of units of R is R \ {0}."
    
    The only counterexample to this statement (when the hypothesis 1 != 0 is dropped)
    is the trivial ring R = {0}.
    """
    h1 = False
    neg_q = False
    
    try:
        # If witness is an integer n, we interpret it as the ring Z/nZ.
        # n = 0 represents Z.
        if isinstance(witness, int):
            if witness >= 0:
                h1 = True
                if witness == 1:
                    neg_q = True
                else:
                    neg_q = False
            return [h1, neg_q]
            
        # If witness is a sympy domain/ring
        if hasattr(witness, 'is_Ring'):
            h1 = bool(witness.is_Ring and witness.is_commutative)
            if hasattr(witness, 'is_zero') and witness.is_zero:
                neg_q = True
            else:
                neg_q = False
            return [h1, neg_q]
            
        # If witness is provided as a collection of elements
        if hasattr(witness, '__len__') and not isinstance(witness, str):
            if len(witness) == 1:
                h1 = True
                neg_q = True
                return [h1, neg_q]
                
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: R is a field if and only if the group of units of R is R \\ {0} (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1
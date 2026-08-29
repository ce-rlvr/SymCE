import sympy

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "The number of primitive n-th roots of unity in C is phi(n)"
    
    The dropped hypothesis is n >= 1.
    For n <= 0, the number of primitive n-th roots of unity is not phi(n)
    (phi(n) is undefined or 0, while the number of roots is phi(-n) > 0 or infinite).
    """
    try:
        # Witness must be an integer
        if isinstance(witness, bool):
            return [False]
            
        if type(witness) not in (int, sympy.Integer):
            if isinstance(witness, float) and witness.is_integer():
                pass
            elif hasattr(witness, 'is_integer') and witness.is_integer:
                pass
            else:
                return [False]
                
        n = int(witness)
        
        # The conclusion holds iff n >= 1.
        # Therefore, the negated conclusion is true iff n <= 0.
        neg_q = (n <= 0)
        
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The number of primitive n-th roots of unity in C is not phi(n)"
]

N_HYP = 0
NEG_Q_INDEX = 0
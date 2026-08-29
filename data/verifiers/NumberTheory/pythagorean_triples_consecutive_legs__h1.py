import math
import sympy

# Top-level setup
# (No named bindings needed for this Number Theory conjecture)

CONDITION_LABELS = [
    "¬Q: There do not exist infinitely many pairs (x, z) satisfying x^2 + (x+1)^2 = z^2"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        # The conclusion is mathematically true (there are infinitely many such pairs, 
        # e.g., (3,5), (20,29), (119,169), etc., derived from Pell's equation).
        # However, if the conjecture was misinterpreted as a universal statement by the platform,
        # the witness might be provided as a counterexample pair (x, z) or a single integer x.
        
        # Case 1: Witness is a pair (x, z), check if it fails the equation
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            try:
                x = int(witness[0])
                z = int(witness[1])
                neg_Q = not (x**2 + (x+1)**2 == z**2)
            except (ValueError, TypeError):
                neg_Q = False
                
        # Case 2: Witness is a single integer x, check if x^2 + (x+1)^2 is NOT a perfect square
        elif isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            x = int(witness)
            val = x**2 + (x+1)**2
            if val < 0:
                neg_Q = True
            else:
                s = int(math.isqrt(val))
                neg_Q = not (s**2 == val)
                
        # Case 3: Witness is a dummy (e.g., None). Evaluate the constant statement.
        # Since there ARE infinitely many pairs, the statement is True, so its negation is False.
        else:
            neg_Q = False
            
    except Exception:
        neg_Q = False
        
    return [neg_Q]
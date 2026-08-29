import sympy
import math

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    """
    try:
        p = int(witness)
        # Restrict to reasonable bounds to ensure fast execution
        if p < 1 or p > 100000:
            return [False]
            
        # Calculate the set of quadratic residues modulo p in {1, ..., p-1}
        residues = set()
        for x in range(p):
            r = (x * x) % p
            if r != 0:
                residues.add(r)
                
        C = len(residues)
        
        # The conclusion is that C == (p - 1) / 2.
        # The negated conclusion is that C != (p - 1) / 2.
        # We use 2 * C != p - 1 to avoid floating point issues.
        neg_q = (2 * C != p - 1)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The number of quadratic residues modulo p in {1, ..., p-1} is not exactly (p-1)/2"
]

N_HYP = 0
NEG_Q_INDEX = 0
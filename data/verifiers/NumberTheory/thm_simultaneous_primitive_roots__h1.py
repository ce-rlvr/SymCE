import sympy
from sympy.ntheory import primitive_root

# Top-level setup
# (No named bindings needed for NumberTheory; use integers directly)

def conditions(witness):
    """
    Given a witness (a list of integers [p_1, p_2, ..., p_k]),
    checks if the conclusion fails.
    
    The conclusion is: "There exists an integer g such that g is a primitive root modulo p_i for all 1 <= i <= k".
    By the generalized Chinese Remainder Theorem and the properties of primitive roots,
    a simultaneous primitive root exists for a set of integers IF AND ONLY IF 
    every integer in the set individually has a primitive root.
    
    Therefore, the conclusion FAILS (neg_Q is True) if and only if at least one p_i 
    does NOT have a primitive root.
    """
    try:
        if not isinstance(witness, (list, tuple)):
            return [False]
            
        if len(witness) == 0:
            # Vacuously true, so the conclusion holds (neg_Q is False)
            return [False]
            
        neg_q = False
        for p in witness:
            if not isinstance(p, int) or p <= 0:
                return [False]
            try:
                # primitive_root(p) raises ValueError if p has no primitive root
                primitive_root(p)
            except ValueError:
                neg_q = True
                break
                
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: There does not exist an integer g such that g is a primitive root modulo p_i for all i"
]
N_HYP = 0
NEG_Q_INDEX = 0
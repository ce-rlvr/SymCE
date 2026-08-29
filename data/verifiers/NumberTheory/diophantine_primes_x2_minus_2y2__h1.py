import sympy

# Top-level setup
# (No specific named objects required for this number theory problem)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture:
    "The equation x^2 - 2y^2 = p has integer solutions x, y if and only if p ≡ 1 (mod 8) or p ≡ 7 (mod 8)."
    """
    try:
        # The witness should be an integer
        if isinstance(witness, bool):
            return [False]
        p = int(witness)
        if p != witness:
            return [False]
    except Exception:
        return [False]
        
    try:
        # Check if x^2 - 2y^2 = p has integer solutions.
        # Since Z[sqrt(2)] is a PID and its fundamental unit 1 + sqrt(2) has norm -1,
        # an integer p can be represented as x^2 - 2y^2 iff the exact power of every 
        # prime factor q ≡ 3, 5 (mod 8) dividing |p| is even.
        if p == 0:
            has_sol = True
        else:
            has_sol = True
            factors = sympy.factorint(abs(p))
            for q, e in factors.items():
                if q % 8 in (3, 5) and e % 2 != 0:
                    has_sol = False
                    break
                    
        # Check the modular condition: p ≡ 1 or 7 (mod 8)
        mod_cond = (p % 8 in (1, 7))
        
        # The conclusion is the equivalence of the two conditions.
        # It fails if one is true and the other is false.
        neg_Q = (has_sol != mod_cond)
        
        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence between x^2 - 2y^2 = p having integer solutions and p ≡ 1, 7 (mod 8) fails"
]

N_HYP = 0
NEG_Q_INDEX = 0
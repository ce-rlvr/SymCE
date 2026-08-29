import sympy as sp

# Top-level setup
# No specific named bindings needed for NumberTheory domain

def conditions(witness):
    """
    Given a witness object, checks if it is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    a = witness
    
    # H_1: a > 1
    try:
        h1 = bool(a > 1)
    except Exception:
        h1 = False
        
    # ¬Q: The strictly positive modular inverse of a modulo a^2 - a + 1 is not a^2 - 2a + 2
    try:
        m = a**2 - a + 1
        inv = a**2 - 2*a + 2
        
        # To be the strictly positive modular inverse:
        # 1. It must be strictly positive.
        is_positive = bool(inv > 0)
        
        # 2. a * inv must be congruent to 1 modulo m.
        # This means (a * inv - 1) / m must be an integer.
        diff = a * inv - 1
        quotient = diff / m
        
        try:
            q_sym = sp.sympify(quotient)
            is_multiple = (int(q_sym) == q_sym)
        except Exception:
            is_multiple = False
            
        # If both conditions hold, then it IS the modular inverse (conclusion holds).
        q_holds = is_positive and is_multiple
    except Exception:
        # If evaluation fails, we consider the conclusion to fail.
        q_holds = False
        
    neg_q = not q_holds
    
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a > 1",
    "¬Q: The strictly positive modular inverse of a modulo a^2 - a + 1 is not a^2 - 2a + 2"
]

N_HYP = 1
NEG_Q_INDEX = 1
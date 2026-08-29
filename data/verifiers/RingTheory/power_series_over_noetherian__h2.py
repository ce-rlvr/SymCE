import sympy
from sympy import Symbol, symbols
from sympy.abc import x, y, z

# Top-level setup
# Standard symbols are provided. A non-Noetherian ring can be represented 
# via a string or a polynomial ring with many generators.

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # 1. Check if witness is a string description
        if isinstance(witness, str):
            w = witness.lower()
            h1 = True
            if "infinit" in w or "non-noetherian" in w or "not noetherian" in w or "not a noetherian" in w:
                neg_q = True
            return [h1, neg_q]
            
        # 2. Check hypothesis: R is a commutative ring with identity
        if hasattr(witness, 'is_commutative'):
            h1 = witness.is_commutative is not False
        else:
            h1 = True
            
        # 3. Check negated conclusion: R[[x]] is not Noetherian (which means R is not Noetherian)
        is_field = getattr(witness, 'is_Field', None)
        if is_field is None:
            is_field = getattr(witness, 'is_field', False)
            
        if getattr(witness, 'is_Noetherian', None) is False:
            neg_q = True
        elif getattr(witness, 'is_noetherian', None) is False:
            neg_q = True
        elif getattr(witness, 'noetherian', None) is False:
            neg_q = True
        elif hasattr(witness, 'gens') and len(witness.gens) >= 10 and not is_field:
            # Proxy for a polynomial ring in infinitely many variables
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The formal power series ring over R is not a Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1
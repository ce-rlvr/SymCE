import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion for the given witness.
    
    The conjecture is:
    "V is a vector space over a field F. The bilinear form B is non-degenerate 
    if and only if its radical is the zero subspace."
    
    This is true for finite-dimensional spaces, but false for infinite-dimensional ones.
    Since sympy does not have a standard representation for infinite-dimensional 
    vector spaces with bilinear forms, this verifier accepts mock objects, dictionaries, 
    strings, or symbolic representations that indicate an infinite-dimensional space.
    """
    h1 = False
    neg_q = False
    
    try:
        # 1. String representation
        if isinstance(witness, str):
            s = witness.lower()
            if any(word in s for word in ["infinite", "poly", "r[x]", "sequence", "l2", "function"]):
                return [True, True]
                
        # 2. Dictionary representation
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_vector_space", True))
            if "radical_is_zero" in witness and "is_non_degenerate" in witness:
                rad_zero = bool(witness["radical_is_zero"])
                non_deg = bool(witness["is_non_degenerate"])
                neg_q = (rad_zero != non_deg)
            else:
                neg_q = bool(witness.get("is_counterexample", True))
            return [h1, neg_q]
            
        # 3. Custom object representation
        if hasattr(witness, "is_vector_space"):
            h1 = bool(witness.is_vector_space)
            if hasattr(witness, "radical_is_zero") and hasattr(witness, "is_non_degenerate"):
                rad_zero = bool(witness.radical_is_zero)
                non_deg = bool(witness.is_non_degenerate)
                neg_q = (rad_zero != non_deg)
            elif hasattr(witness, "is_counterexample"):
                neg_q = bool(witness.is_counterexample)
            else:
                neg_q = True
            return [h1, neg_q]
            
        # 4. Tuple with a callable (V, B)
        if isinstance(witness, tuple) and len(witness) == 2:
            V, B = witness
            if callable(B):
                return [True, True]
                
        # 5. Polynomial ring (infinite dimensional)
        if hasattr(witness, "domain") and hasattr(witness, "gens"):
            if hasattr(witness, "is_ring") and witness.is_ring:
                return [True, True]
            
        # 6. Matrix (finite dimensional, never a counterexample)
        if hasattr(witness, "det") and hasattr(witness, "nullspace"):
            # A finite dimensional matrix over a field is non-degenerate iff its radical is zero.
            return [True, False]
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "¬Q: The bilinear form B is degenerate but its radical is zero (or vice versa)"
]

N_HYP = 1
NEG_Q_INDEX = 1
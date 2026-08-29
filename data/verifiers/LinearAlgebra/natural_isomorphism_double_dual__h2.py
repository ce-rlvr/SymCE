import sympy
from sympy import oo
from sympy.abc import x, y, z

# Top-level setup
R1 = "R^1"
R2 = "R^2"
R3 = "R^3"
R_n = "R^n"
R_poly = "R[x]"
l2 = "l^2"
R_oo = "R^oo"

def conditions(witness) -> list[bool]:
    is_vs = False
    neg_q = False
    
    try:
        # If witness is SymPy infinity, it represents an infinite-dimensional space
        if witness == sympy.oo:
            return [True, True]
            
        # If witness is an integer, it represents the dimension of the space
        if isinstance(witness, int):
            if witness >= 0:
                return [True, False]
            return [False, False]
            
        # If witness is a string descriptor
        if isinstance(witness, str):
            s = witness.lower()
            if any(sub in s for sub in ["oo", "inf", "[", "poly", "l2", "l^2", "c(", "c["]):
                return [True, True]
            return [True, False]
            
        # If witness is a SymPy Symbol
        if isinstance(witness, sympy.Symbol):
            s = witness.name.lower()
            if any(sub in s for sub in ["oo", "inf", "poly"]):
                return [True, True]
            return [True, False]
            
        # If witness is a polynomial ring (infinite-dimensional)
        if hasattr(witness, 'gens') and hasattr(witness, 'domain'):
            s = str(witness).lower()
            # Exclude finite-dimensional quotient rings
            if "quo" in s or "/" in s or "mod" in s:
                return [True, False]
            return [True, True]
            
        # If witness is a Matrix (representing a finite-dimensional column space)
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            return [True, False]
            
        # If witness is a collection
        if isinstance(witness, (tuple, list, set)):
            s = str(witness).lower()
            if any(sub in s for sub in ["oo", "inf", "poly", "[x]"]):
                return [True, True]
            return [True, False]
            
        # Fallback for other SymPy objects
        if isinstance(witness, sympy.Basic):
            s = str(witness).lower()
            if any(sub in s for sub in ["poly", "oo", "inf", "[x]"]):
                return [True, True]
            return [True, False]
            
    except Exception:
        pass
        
    return [is_vs, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "¬Q: The evaluation map is not an isomorphism (V is infinite-dimensional)"
]

N_HYP = 1
NEG_Q_INDEX = 1
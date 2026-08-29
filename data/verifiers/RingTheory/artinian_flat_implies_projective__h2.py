import sympy
from sympy import S

# Top-level setup: Named objects for the witness expression to reference
Z = "Z"
Q = "Q"
Z2 = "Z/2Z"
Z3 = "Z/3Z"
Z4 = "Z/4Z"
Z6 = "Z/6Z"
Z8 = "Z/8Z"
Z9 = "Z/9Z"
Zp = "Z/pZ"
Zp2 = "Z/p^2Z"

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a right Artinian ring, then M is a projective right R-module."
    
    The witness should be a tuple (R, M) representing the ring and the module.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get("R", witness.get("ring", None))
            M = witness.get("M", witness.get("module", None))
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            R = witness
            M = None
            
        R_str = str(R).strip()
        M_str = str(M).strip()
        
        # Hypothesis 1: R is a right Artinian ring
        artinian_rings = {
            "Z/4Z", "Z/8Z", "Z/9Z", "Z/p^2Z", "Q", "R", "C", 
            "GF(2)", "GF(3)", "Z/2Z", "Z/3Z", "Z/6Z", "k[x]/(x^2)", 
            "Rationals", "Reals", "Complexes", "QQ", "RR", "CC"
        }
        non_artinian_rings = {
            "Z", "Q[x]", "Z[x]", "R[x]", "C[x]", "ZZ", "Integers"
        }
        
        h1 = False
        if R_str in artinian_rings:
            h1 = True
        elif R_str in non_artinian_rings:
            h1 = False
        else:
            h1 = False
            
        # Conclusion: M is a projective right R-module
        # We want this to FAIL (so neg_q should be True when M is NOT projective)
        fields = {
            "Q", "R", "C", "GF(2)", "GF(3)", "Z/2Z", "Z/3Z", "Z/pZ",
            "QQ", "RR", "CC", "Rationals", "Reals", "Complexes"
        }
        
        if R_str in fields:
            is_proj = True
        elif R_str == "Z/4Z" and M_str == "Z/2Z":
            is_proj = False
        elif R_str == "Z/8Z" and M_str in ["Z/2Z", "Z/4Z"]:
            is_proj = False
        elif R_str == "Z/9Z" and M_str == "Z/3Z":
            is_proj = False
        elif R_str == "Z/p^2Z" and M_str == "Z/pZ":
            is_proj = False
        elif R_str == "k[x]/(x^2)" and M_str == "k":
            is_proj = False
        elif R_str == M_str:
            is_proj = True
        else:
            # Default to True to avoid false positives for neg_Q
            is_proj = True
            
        neg_q = not is_proj
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: M is not a projective right R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1
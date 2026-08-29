import sympy
from sympy import ZZ, QQ, Symbol

# Top-level setup for potential witness expressions
Z = "Z"
Q = "Q"
Z_2Z = "Z/2Z"
Q_Z = "Q/Z"
Q_x = "Q[x]"
Z_x = "Z[x]"
Q_fx = "Q(x)"

def conditions(witness) -> list[bool]:
    """
    Given a witness (R, E), checks if it is a counterexample to the false conjecture:
    "Every R-module E over a PID R is injective."
    
    Returns:
        [H_1_ok, H_2_ok, neg_Q_ok]
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, E = witness
        elif isinstance(witness, str):
            parts = [p.strip() for p in witness.split(',')]
            if len(parts) == 2:
                R, E = parts
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        R_str = str(R).strip()
        E_str = str(E).strip()
        
        # H1: R is a principal ideal domain
        h1 = False
        if R_str in ["Z", "ZZ", "Integers", "Q", "QQ", "Rationals", "Q[x]", "QQ[x]", "R[x]"]:
            h1 = True
        elif hasattr(R, 'is_PrincipalIdealDomain') and R.is_PrincipalIdealDomain:
            h1 = True
            
        # H2: E is an R-module
        h2 = False
        if R_str in ["Z", "ZZ", "Integers"]:
            if E_str in ["Z", "ZZ", "Integers", "Q", "QQ", "Rationals", "Z/2Z", "Z_2", "Z2", "Q/Z", "Z[x]", "ZZ[x]", "Q[x]", "QQ[x]"]:
                h2 = True
        elif R_str in ["Q", "QQ", "Rationals"]:
            if E_str in ["Q", "QQ", "Rationals", "Q[x]", "QQ[x]"]:
                h2 = True
        elif R_str in ["Q[x]", "QQ[x]"]:
            if E_str in ["Q[x]", "QQ[x]", "Q(x)", "QQ(x)"]:
                h2 = True
                
        # neg_Q: E is NOT an injective R-module
        # Over a PID, an R-module is injective iff it is divisible.
        neg_q = False
        if R_str in ["Z", "ZZ", "Integers"]:
            if E_str in ["Z", "ZZ", "Integers", "Z/2Z", "Z_2", "Z2", "Z[x]", "ZZ[x]"]:
                neg_q = True  # Not divisible, hence not injective
            elif E_str in ["Q", "QQ", "Rationals", "Q/Z", "Q[x]", "QQ[x]"]:
                neg_q = False # Divisible, hence injective
        elif R_str in ["Q", "QQ", "Rationals"]:
            if E_str in ["Q", "QQ", "Rationals", "Q[x]", "QQ[x]"]:
                neg_q = False # Vector spaces over fields are injective
        elif R_str in ["Q[x]", "QQ[x]"]:
            if E_str in ["Q[x]", "QQ[x]"]:
                neg_q = True  # Not divisible by x
            elif E_str in ["Q(x)", "QQ(x)"]:
                neg_q = False # Field of fractions is divisible
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: E is an R-module",
    "¬Q: E is not an injective R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2
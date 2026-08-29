import sympy
from sympy.polys.domains import CC, QQ, RR, ZZ

def conditions(witness):
    try:
        K, F = witness
    except Exception:
        return [False, False]
    
    # H_1: K is an algebraically closed field
    try:
        # In SymPy, CC is the only algebraically closed field domain.
        h1_ok = bool(getattr(K, 'is_Field', False) and K == CC)
    except Exception:
        h1_ok = False
        
    # ¬Q: There exists a field homomorphism from K to F
    try:
        # A field homomorphism exists iff K embeds into F.
        # For SymPy domains, F.unify(K) == F means K is a subfield of F.
        neg_q_ok = bool(getattr(F, 'is_Field', False) and F.unify(K) == F)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "¬Q: There exists a field homomorphism from K to F"
]

N_HYP = 1
NEG_Q_INDEX = 1
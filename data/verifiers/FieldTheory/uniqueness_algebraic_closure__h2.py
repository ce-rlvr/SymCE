import sympy
from sympy.polys.domains import QQ, RR, CC, ZZ

# Top-level setup
# The witness should be a tuple (F, K1, K2)
# Example witness: (RR, QQ, CC) or (RR, RR, CC)

def conditions(witness) -> list[bool]:
    try:
        F, K1, K2 = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False
        
    # H_2: K2 is an algebraic closure of F
    try:
        h2 = False
        if getattr(F, 'is_Field', False) and getattr(K2, 'is_Field', False):
            fname = getattr(F, 'name', '')
            k2name = getattr(K2, 'name', '')
            # In SymPy's domains, CC is the algebraic closure of RR and CC.
            if k2name == 'CC' and fname in ('RR', 'CC'):
                h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: There does not exist a field isomorphism from K1 to K2 fixing F
    try:
        # In our restricted domain of SymPy fields, CC is the only algebraic closure.
        # Any field isomorphic to CC must be CC itself.
        # Therefore, if K1 != K2, they are not isomorphic.
        neg_q = bool(K1 != K2)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K2 is an algebraic closure of F",
    "¬Q: There does not exist a field isomorphism from K1 to K2 fixing F"
]

N_HYP = 2
NEG_Q_INDEX = 2
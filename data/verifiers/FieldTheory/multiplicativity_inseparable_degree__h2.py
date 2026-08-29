import sympy

# Top-level setup
# Witness is expected to be a dictionary with keys:
# 'is_tower': bool
# 'insep_deg_KF': float or int
# 'insep_deg_KE': float or int
# 'insep_deg_EF': float or int

def conditions(witness):
    try:
        if not isinstance(witness, dict):
            return [False, False]
        
        h1 = bool(witness.get('is_tower', False))
        
        kf = witness.get('insep_deg_KF')
        ke = witness.get('insep_deg_KE')
        ef = witness.get('insep_deg_EF')
        
        if kf is None or ke is None or ef is None:
            return [False, False]
            
        neg_q = bool(kf != ke * ef)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: F is a subfield of E and E is a subfield of K",
    "¬Q: insep_deg(K/F) != insep_deg(K/E) * insep_deg(E/F)"
]

N_HYP = 1
NEG_Q_INDEX = 1
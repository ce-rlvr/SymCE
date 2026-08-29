import sympy
from sympy import S

R = "reals"
C = "complexes"
Q = "rationals"
H = "quaternions"

CONDITION_LABELS = [
    "H_1: D is a finite-dimensional central division algebra over K",
    "¬Q: D is not isomorphic to K (or Br(K) is not trivial)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def _identify_algebra(obj):
    if obj in [H, "quaternions"]: 
        return "H"
    if getattr(obj, "__name__", "") == "Quaternion": 
        return "H"
    if obj in [R, "reals", S.Reals]: 
        return "R"
    if obj in [C, "complexes", S.Complexes]: 
        return "C"
    if obj in [Q, "rationals", S.Rationals]: 
        return "Q"
    return None

def _identify_field(obj):
    if obj in [R, "reals", S.Reals]: 
        return "R"
    if obj in [C, "complexes", S.Complexes]: 
        return "C"
    if obj in [Q, "rationals", S.Rationals]: 
        return "Q"
    return None

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            K_obj, D_obj = witness
            K_id = _identify_field(K_obj)
            D_id = _identify_algebra(D_obj)
        else:
            D_obj = witness
            D_id = _identify_algebra(D_obj)
            if D_id == "H":
                K_id = "R"
            elif D_id in ["R", "C", "Q"]:
                K_id = D_id
            else:
                K_id = None
    except Exception:
        return [False, False]
        
    try:
        h1 = False
        if K_id == "R" and D_id in ["R", "H"]:
            h1 = True
        elif K_id == "C" and D_id == "C":
            h1 = True
        elif K_id == "Q" and D_id == "Q":
            h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        if h1:
            neg_q = (K_id != D_id)
    except Exception:
        neg_q = False

    return [h1, neg_q]
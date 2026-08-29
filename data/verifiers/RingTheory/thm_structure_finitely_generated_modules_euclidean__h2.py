import sympy
from sympy import S

# Top-level setup
Z = S.Integers
Q = S.Rationals
R = S.Reals
C = S.Complexes

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R_obj = witness.get("R", "Z")
            M_obj = witness.get("M", "Q")
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            R_obj, M_obj = witness
        else:
            R_obj = "Z"
            M_obj = witness
            
        def to_str(obj):
            if obj == S.Integers: return "Z"
            if obj == S.Rationals: return "Q"
            if obj == S.Reals: return "R"
            if obj == S.Complexes: return "C"
            s = str(obj).replace(" ", "")
            if s == "ZZ": return "Z"
            if s == "QQ": return "Q"
            if s == "RR": return "R"
            if s == "CC": return "C"
            return s
            
        R_str = to_str(R_obj)
        M_str = to_str(M_obj)
        
        # H1: R is a Euclidean domain
        euclidean = {"Z", "Q", "R", "C", "Q[x]", "R[x]", "C[x]", "F_p", "F_p[x]", "Z[i]"}
        h1 = R_str in euclidean
        
        # neg_Q: M is NOT isomorphic to a direct sum of a free R-module and a finite number of cyclic torsion R-modules
        neg_q = False
        
        if R_str in {"Q", "R", "C", "F_p", "QQ", "RR", "CC"}:
            neg_q = False
        elif M_str in {R_str, R_str + "^2", R_str + "^3", R_str + "[x]"}:
            neg_q = False
        elif R_str == "Z":
            if M_str in {
                "Q", "R", "C", "Q/Z", "R/Z", "Z[1/2]", "Z[1/p]", "Q_p", "Z_p", 
                "Q(x)", "R(x)", "QQ", "RR", "CC", "Z(p^infty)", "Z(p^oo)", 
                "Z[1/p]/Z", "Z^N", "Z^infty", "Z^oo", "(Z/2Z)^N", "(Z/2Z)^infty",
                "Q^2", "Q^n", "R^2", "R^n"
            }:
                neg_q = True
            elif M_str in {"Z/2Z", "Z/3Z", "Z/4Z", "Z/nZ"}:
                neg_q = False
        elif R_str in {"Q[x]", "R[x]", "C[x]", "F_p[x]"}:
            F = R_str.replace("[x]", "")
            if M_str in {f"{F}(x)", f"{F}[[x]]", f"{F}[x,y]"}:
                neg_q = True
        elif R_str == "Z[i]":
            if M_str in {"Q(i)", "C"}:
                neg_q = True
                
    except Exception:
        h1 = False
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: M is not isomorphic to the direct sum of a free R-module and a finite number of cyclic torsion R-modules"
]

N_HYP = 1
NEG_Q_INDEX = 1
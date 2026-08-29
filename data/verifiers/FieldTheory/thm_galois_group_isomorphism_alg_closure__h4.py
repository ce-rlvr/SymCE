import sympy
from sympy import S

# Top-level setup
QQ = "QQ"
RR = "RR"
CC = "CC"
QQ_bar = "QQ_bar"
QQ_sqrt2 = "QQ(sqrt(2))"
QQ_cbrt2 = "QQ(2**(1/3))"
QQ_i = "QQ(i)"
F2 = "F2"
F2_bar = "F2_bar"
Fp = "Fp"
Fp_bar = "Fp_bar"

def get_name(obj):
    if obj == S.Rationals: return "QQ"
    if obj == S.Reals: return "RR"
    if obj == S.Complexes: return "CC"
    
    s = str(obj).replace(" ", "")
    if "2**(1/3)" in s or "cbrt(2)" in s:
        return "QQ(2**(1/3))"
    if "sqrt(2)" in s or "2**(1/2)" in s:
        return "QQ(sqrt(2))"
    if "QQ(i)" in s or "QQ<I>" in s:
        return "QQ(i)"
    if "QQ_bar" in s or "Algebraic" in s:
        return "QQ_bar"
    if s == "CC" or "Complexes" in s:
        return "CC"
    if s == "RR" or "Reals" in s:
        return "RR"
    if s == "QQ" or "Rationals" in s:
        return "QQ"
    if "F2_bar" in s: return "F2_bar"
    if "F2" in s: return "F2"
    if "Fp_bar" in s: return "Fp_bar"
    if "Fp" in s: return "Fp"
    return s

FIELDS = {
    "QQ": {"is_field": True, "is_alg_closed": False},
    "RR": {"is_field": True, "is_alg_closed": False},
    "CC": {"is_field": True, "is_alg_closed": True},
    "QQ_bar": {"is_field": True, "is_alg_closed": True},
    "QQ(sqrt(2))": {"is_field": True, "is_alg_closed": False},
    "QQ(2**(1/3))": {"is_field": True, "is_alg_closed": False},
    "QQ(i)": {"is_field": True, "is_alg_closed": False},
    "F2": {"is_field": True, "is_alg_closed": False},
    "F2_bar": {"is_field": True, "is_alg_closed": True},
    "Fp": {"is_field": True, "is_alg_closed": False},
    "Fp_bar": {"is_field": True, "is_alg_closed": True},
}

def contains(A, B):
    A = get_name(A)
    B = get_name(B)
    if A == B: return True
    if A == "CC":
        return B in ["RR", "QQ", "QQ(sqrt(2))", "QQ(2**(1/3))", "QQ_bar", "QQ(i)"]
    if A == "QQ_bar":
        return B in ["QQ", "QQ(sqrt(2))", "QQ(2**(1/3))", "QQ(i)"]
    if A == "RR":
        return B in ["QQ", "QQ(sqrt(2))", "QQ(2**(1/3))"]
    if A in ["QQ(sqrt(2))", "QQ(2**(1/3))", "QQ(i)"]:
        return B == "QQ"
    if A == "F2_bar" and B == "F2": return True
    if A == "Fp_bar" and B == "Fp": return True
    return False

def is_normal(K, F):
    K = get_name(K)
    F = get_name(F)
    if K == F: return True
    if F == "QQ":
        if K in ["QQ(sqrt(2))", "QQ(i)", "QQ_bar", "CC"]: return True
        if K == "QQ(2**(1/3))": return False
    if F == "RR" and K == "CC": return True
    if F == "F2" and K == "F2_bar": return True
    if F == "Fp" and K == "Fp_bar": return True
    return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        F, E, K = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        F_name = get_name(F)
        h1 = FIELDS.get(F_name, {}).get("is_field", False)
    except Exception:
        h1 = False

    try:
        E_name = get_name(E)
        h2 = FIELDS.get(E_name, {}).get("is_field", False) and \
             FIELDS.get(E_name, {}).get("is_alg_closed", False) and \
             contains(E_name, F_name)
    except Exception:
        h2 = False

    try:
        K_name = get_name(K)
        h3 = FIELDS.get(K_name, {}).get("is_field", False) and \
             contains(E_name, K_name) and \
             contains(K_name, F_name)
    except Exception:
        h3 = False

    try:
        # The conclusion fails if K is not normal over F.
        # In that case, Aut(E/K) is not a normal subgroup of Aut(E/F),
        # so the quotient is not a group and cannot be isomorphic to Gal(K/F).
        neg_q = not is_normal(K_name, F_name)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an algebraically closed field containing F",
    "H_3: K is a subfield of E containing F",
    "¬Q: Gal(K/F) is not isomorphic to Aut(E/F) / Aut(E/K) (e.g. K is not normal over F)"
]

N_HYP = 3
NEG_Q_INDEX = 3
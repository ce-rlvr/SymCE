import sympy
from sympy import S

# Top-level setup
Z = "Z"
Q = "Q"
R_ring = "R"
C_ring = "C"
Z2 = "Z2"
Z_oplus_Z2 = "Z_oplus_Z2"
Z_oplus_Z = "Z_oplus_Z"
Q_oplus_Z = "Q_oplus_Z"
Q_x = "Q[x]"
Q_x_frac = "Q(x)"
Z_x = "Z[x]"

rings = {
    "Z": {"is_PID": True},
    "Q": {"is_PID": True},
    "R": {"is_PID": True},
    "C": {"is_PID": True},
    "Q[x]": {"is_PID": True},
    "R[x]": {"is_PID": True},
    "C[x]": {"is_PID": True},
    "Z[x]": {"is_PID": False},
    "Q[x,y]": {"is_PID": False}
}

modules = {
    ("Z", "Z"): {"torsion_free": True, "injective_double_dual": True},
    ("Z", "Q"): {"torsion_free": True, "injective_double_dual": False},
    ("Z", "R"): {"torsion_free": True, "injective_double_dual": False},
    ("Z", "C"): {"torsion_free": True, "injective_double_dual": False},
    ("Z", "Z2"): {"torsion_free": False, "injective_double_dual": False},
    ("Z", "Z_oplus_Z2"): {"torsion_free": False, "injective_double_dual": False},
    ("Z", "Z_oplus_Z"): {"torsion_free": True, "injective_double_dual": True},
    ("Z", "Q_oplus_Z"): {"torsion_free": True, "injective_double_dual": False},
    ("Z", "Z[1/p]"): {"torsion_free": True, "injective_double_dual": False},
    ("Z", "Q/Z"): {"torsion_free": False, "injective_double_dual": False},
    ("Q", "Q"): {"torsion_free": True, "injective_double_dual": True},
    ("Q", "Q_oplus_Q"): {"torsion_free": True, "injective_double_dual": True},
    ("Q[x]", "Q[x]"): {"torsion_free": True, "injective_double_dual": True},
    ("Q[x]", "Q(x)"): {"torsion_free": True, "injective_double_dual": False},
    ("Z[x]", "Z[x]"): {"torsion_free": True, "injective_double_dual": True},
}

def parse_ring(R):
    if isinstance(R, str): return R
    if R == S.Integers: return "Z"
    if R == S.Rationals: return "Q"
    if R == S.Reals: return "R"
    if R == S.Complexes: return "C"
    return str(R)

def parse_module(M):
    if isinstance(M, str): return M
    if M == S.Integers: return "Z"
    if M == S.Rationals: return "Q"
    if M == S.Reals: return "R"
    if M == S.Complexes: return "C"
    return str(M)

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            R, M = witness
        elif isinstance(witness, str):
            R = "Z"
            M = witness
        elif isinstance(witness, dict) and "R" in witness and "M" in witness:
            R = witness["R"]
            M = witness["M"]
        else:
            R = "Z"
            M = witness
    except Exception:
        return [False, False]
        
    try:
        R_str = parse_ring(R)
        h1 = rings[R_str]["is_PID"]
    except Exception:
        h1 = False
        
    try:
        R_str = parse_ring(R)
        M_str = parse_module(M)
        mod_info = modules[(R_str, M_str)]
        is_inj = mod_info["injective_double_dual"]
        is_tf = mod_info["torsion_free"]
        conclusion = (is_inj == is_tf)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: The equivalence between M -> M** being injective and M being torsion-free fails"
]

N_HYP = 1
NEG_Q_INDEX = 1
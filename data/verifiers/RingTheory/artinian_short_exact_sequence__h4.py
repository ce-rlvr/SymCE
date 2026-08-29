import sympy
from sympy import Rational, Integer

# Top-level setup
Z = "Z"
Q = "Q"
R_ring = "R"
C_ring = "C"

M_0 = "0"
M_Z = "Z"
M_Q = "Q"
M_Q_Z = "Q/Z"
M_Z2 = "Z_2"
M_Z4 = "Z_4"

def parse_ring(R):
    R_str = str(R).replace(" ", "")
    if R_str in ["Z", "Integers", "ZZ", "S.Integers"]: return "Z"
    if R_str in ["Q", "Rationals", "QQ", "S.Rationals"]: return "Q"
    if R_str in ["R", "Reals", "RR", "S.Reals"]: return "R"
    if R_str in ["C", "Complexes", "CC", "S.Complexes"]: return "C"
    return R_str

def parse_module(M):
    M_str = str(M).replace(" ", "")
    if M_str in ["0", "Zero", "S.Zero"]: return "0"
    if M_str in ["Z", "Integers", "ZZ", "S.Integers"]: return "Z"
    if M_str in ["Q", "Rationals", "QQ", "S.Rationals"]: return "Q"
    if "p^infty" in M_str or "p^infinity" in M_str: return "Z(p^infty)"
    return M_str

def is_ring(R):
    return R in ["Z", "Q", "R", "C", "k[x]"]

def is_module(R, M):
    if R == "Z":
        if M in ["0", "Z", "Q", "Q/Z", "Z(p^infty)"]: return True
        if M.startswith("Z_"): return True
        if M.startswith("Z^"): return True
        return False
    if R in ["Q", "R", "C"]:
        if M == "0": return True
        if M == R: return True
        if M == R + "^2": return True
        if M == R + "^3": return True
        return False
    return False

def is_exact(R, m1, m2, m3):
    if not (is_module(R, m1) and is_module(R, m2) and is_module(R, m3)):
        return False
    # Isomorphism cases
    if m1 == "0" and m2 == m3: return True
    if m3 == "0" and m1 == m2: return True
    
    if R == "Z":
        if m1 == "Z" and m2 == "Z" and m3.startswith("Z_"): return True
        if m1 == "Z" and m2 == "Z^2" and m3 == "Z": return True
        if m1 == "Z" and m2 == "Q" and m3 == "Q/Z": return True
        if m1.startswith("Z_") and m2.startswith("Z_") and m3.startswith("Z_"):
            try:
                n1 = int(m1[2:])
                n2 = int(m2[2:])
                n3 = int(m3[2:])
                if n2 == n1 * n3: return True
            except Exception:
                pass
    if R in ["Q", "R", "C"]:
        def dim(m):
            if m == "0": return 0
            if m == R: return 1
            if m == R + "^2": return 2
            if m == R + "^3": return 3
            return -1
        d1, d2, d3 = dim(m1), dim(m2), dim(m3)
        if d1 >= 0 and d2 >= 0 and d3 >= 0 and d2 == d1 + d3:
            return True
    return False

def is_artinian(R, M):
    if not is_module(R, M): return False
    if R == "Z":
        if M == "0": return True
        if M == "Z": return False
        if M.startswith("Z^"): return False
        if M == "Q": return False
        if M == "Q/Z": return False
        if M == "Z(p^infty)": return True
        if M.startswith("Z_"): return True
    if R in ["Q", "R", "C"]:
        if M in ["0", R, R + "^2", R + "^3"]: return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        R_raw, m1_raw, m2_raw, m3_raw = witness
        R = parse_ring(R_raw)
        m1 = parse_module(m1_raw)
        m2 = parse_module(m2_raw)
        m3 = parse_module(m3_raw)
        
        h1 = is_ring(R)
        h2 = is_exact(R, m1, m2, m3)
        h3 = is_artinian(R, m1)
        
        neg_q = not is_artinian(R, m2)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: 0 -> M' -> M -> M'' -> 0 is a short exact sequence of R-modules",
    "H_3: M' is an Artinian R-module",
    "¬Q: M is not an Artinian R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3
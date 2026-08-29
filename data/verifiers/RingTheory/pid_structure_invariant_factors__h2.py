import sympy
from sympy import QQ, ZZ, RR, CC
from sympy.abc import x, y
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_pid(R):
    if hasattr(R, 'is_PID'):
        if R.is_PID is not None:
            return bool(R.is_PID)
            
    R_str = str(R).replace(" ", "")
    if R_str in ["Z", "Q", "R", "C", "Z[i]", "ZZ", "QQ", "RR", "CC", "Z[1/2]", "Z[1/p]"]:
        return True
    if R_str in ["Q[x]", "R[x]", "C[x]", "F2[x]", "F3[x]", "Fp[x]", "QQ[x]", "RR[x]", "CC[x]", "k[x]"]:
        return True
    if R_str in ["Z[x]", "Q[x,y]", "R[x,y]", "C[x,y]", "Z[sqrt(-5)]", "Z[x,y]", "ZZ[x]", "QQ[x,y]", "k[x,y]"]:
        return False
        
    if hasattr(R, 'is_PolyRing'):
        if R.domain.is_Field and len(R.gens) == 1:
            return True
        else:
            return False
            
    return False

def check_fg(M, R):
    if M == R:
        return True
        
    if R == ZZ or str(R) == "ZZ":
        if M in [QQ, RR, CC] or str(M) in ["QQ", "RR", "CC"]:
            return False
            
    if R == QQ or str(R) == "QQ":
        if M in [RR, CC] or str(M) in ["RR", "CC"]:
            return False
            
    if hasattr(R, 'is_PolyRing') and hasattr(M, 'is_FractionField'):
        if M.ring == R:
            return False
            
    M_str = str(M).replace(" ", "")
    R_str = str(R).replace(" ", "")
    
    M_str = M_str.replace("ZZ", "Z").replace("QQ", "Q").replace("RR", "R").replace("CC", "C")
    R_str = R_str.replace("ZZ", "Z").replace("QQ", "Q").replace("RR", "R").replace("CC", "C")
    
    NON_FG = {
        "Z": ["Q", "Q/Z", "Z[1/2]", "Z[1/3]", "Z[1/p]", "R", "C", "Z^N", "Z^(N)", "Q[x]", "R[x]", "C[x]", "Z[x]", "Z[1/2,1/3]"],
        "Q": ["R", "C", "Q^N", "Q^(N)", "Q[x]", "R[x]", "C[x]"],
        "R": ["R[x]", "C[x]", "R^N", "R^(N)"],
        "C": ["C[x]", "C^N", "C^(N)"],
        "Q[x]": ["Q[x,y]", "Q[x]^N", "Q[x]^(N)", "Q(x)"],
        "R[x]": ["R[x,y]", "R[x]^N", "R[x]^(N)", "R(x)"],
        "C[x]": ["C[x,y]", "C[x]^N", "C[x]^(N)", "C(x)"],
        "k[x]": ["k[x,y]", "k[x]^N", "k[x]^(N)", "k(x)"],
        "Z[i]": ["Q(i)", "Z[i]^N", "Z[i]^(N)"]
    }

    FG = {
        "Z": ["Z", "Z^2", "Z^3", "Z/2Z", "Z/3Z", "Z/4Z", "Z/6Z", "Z[i]"],
        "Q": ["Q", "Q^2", "Q^3", "Q[sqrt(2)]"],
        "R": ["R", "C", "R^2", "R^3"],
        "C": ["C", "C^2", "C^3"],
        "Q[x]": ["Q[x]", "Q[x]^2", "Q[x]/(x^2+1)"],
        "R[x]": ["R[x]", "R[x]^2", "R[x]/(x^2+1)"],
        "C[x]": ["C[x]", "C[x]^2", "C[x]/(x-1)"],
        "Z[i]": ["Z[i]", "Z[i]^2", "Z[i]/(2)"]
    }
    
    if R_str in NON_FG and M_str in NON_FG[R_str]:
        return False
    if R_str in FG and M_str in FG[R_str]:
        return True
        
    if "^N" in M_str or "^(N)" in M_str or "infty" in M_str:
        return False
        
    if M_str.startswith(R_str + "^"):
        power = M_str.split("^")[1]
        if power.isdigit():
            return True
            
    if M_str == R_str.replace("[", "(").replace("]", ")"):
        return False
        
    if M_str.startswith(R_str + "/") or M_str.startswith(R_str + "^"):
        if "^N" not in M_str and "^(N)" not in M_str and "infty" not in M_str:
            return True
            
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (R, M), a dict {"R": R, "M": M}, or a string "M over R".
    If only M is provided, R defaults to Z.
    """
    R = None
    M = None
    
    if isinstance(witness, tuple) and len(witness) == 2:
        R, M = witness
    elif isinstance(witness, dict):
        R = witness.get("R", None)
        M = witness.get("M", None)
    elif isinstance(witness, str):
        if " over " in witness:
            M_str, R_str = witness.split(" over ")
            M, R = M_str.strip(), R_str.strip()
        else:
            M = witness.strip()
            R = "Z"
    elif hasattr(witness, 'is_Domain') or hasattr(witness, 'is_Ring') or hasattr(witness, 'is_Field'):
        M = witness
        R = ZZ
        
    if R is None or M is None:
        return [False, False]
        
    try:
        h1_ok = check_pid(R)
    except Exception:
        h1_ok = False
        
    try:
        is_finitely_generated = check_fg(M, R)
        neg_q = not is_finitely_generated
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: M is not isomorphic to R^r \\oplus R/(a_1) \\oplus \\dots \\oplus R/(a_m) (i.e. M is not finitely generated)"
]

N_HYP = 1
NEG_Q_INDEX = 1
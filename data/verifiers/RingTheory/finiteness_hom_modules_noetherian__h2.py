import sympy
from sympy import *
import re

# Top-level setup
# Define some common string constants that might be used in witness expressions
Z = "Z"
Q = "Q"
R_field = "R"
C = "C"
Z_infty_sum = "Z_infty_sum"
Z_infty_prod = "Z_infty_prod"

def get_R_M_N(witness):
    """Extract R, M, N from the witness object."""
    if isinstance(witness, dict):
        return str(witness.get("R", "")), str(witness.get("M", "")), str(witness.get("N", ""))
    if isinstance(witness, tuple) and len(witness) == 3:
        return str(witness[0]), str(witness[1]), str(witness[2])
    if hasattr(witness, "R") and hasattr(witness, "M") and hasattr(witness, "N"):
        return str(witness.R), str(witness.M), str(witness.N)
    if isinstance(witness, str):
        R_match = re.search(r'R\s*=\s*([^,]+)', witness)
        M_match = re.search(r'M\s*=\s*([^,]+)', witness)
        N_match = re.search(r'N\s*=\s*([^,]+)', witness)
        R = R_match.group(1).strip() if R_match else ""
        M = M_match.group(1).strip() if M_match else ""
        N = N_match.group(1).strip() if N_match else ""
        if R and M and N:
            return R, M, N
        parts = witness.split(',')
        if len(parts) == 3:
            return parts[0].strip(), parts[1].strip(), parts[2].strip()
    return "", "", ""

def is_comm_noeth(R):
    R = str(R).strip()
    if R in ["Z", "Q", "R", "C", "Z[x]", "k[x]", "Z_p", "Z/nZ", "Z/2Z", "Integers", "Rationals", "Reals", "Complexes"]: 
        return True
    if R in ["k[x_1, x_2, ...]", "Z[x_1, x_2, ...]"]: 
        return False
    return False

def is_fg(R, N):
    R = str(R).strip()
    N = str(N).strip()
    if R in ["Z", "Integers"]:
        if N in ["Z", "Z^n", "0", "Z/2Z", "Z/nZ", "Integers"]: 
            return True
        if N in ["Q", "R", "C", "Z_infty_sum", "Z_infty_prod", "Q/Z", "Z[x]", "Z[x,y]", "Rationals", "Reals", "Complexes"]: 
            return False
    if R in ["Q", "R", "C", "Rationals", "Reals", "Complexes"]:
        if N in ["Q", "R", "C", "0", "Q^n", "R^n", "C^n", "Rationals", "Reals", "Complexes"]: 
            return True
        if N in ["Q_infty_sum", "R_infty_sum", "C_infty_sum"]: 
            return False
    return False

def is_hom_fg(R, M, N):
    R = str(R).strip()
    M = str(M).strip()
    N = str(N).strip()
    if R in ["Z", "Integers"]:
        if M in ["Z_infty_sum", "Z[x]", "Z[x,y]"] and N in ["Z", "Z^n", "Z/2Z", "Z/nZ", "Integers"]:
            return False
        if M == "Z_infty_prod" and N in ["Z", "Integers"]:
            return False
        if M in ["Q", "Rationals"] and N in ["Z", "Integers"]:
            return True
    if R in ["Q", "R", "C", "Rationals", "Reals", "Complexes"]:
        if M in ["Q_infty_sum", "R_infty_sum", "C_infty_sum"] and N in ["Q", "R", "C", "Rationals", "Reals", "Complexes"]:
            return False
    # Default to True (meaning it IS finitely generated, so it fails as a counterexample) if unknown
    return True

def conditions(witness) -> list[bool]:
    try:
        R, M, N = get_R_M_N(witness)
    except Exception:
        R, M, N = "", "", ""

    try:
        h1 = is_comm_noeth(R)
    except Exception:
        h1 = False

    try:
        h2 = is_fg(R, N)
    except Exception:
        h2 = False

    try:
        # neg_Q is True if Hom_R(M, N) is NOT finitely generated
        neg_q = not is_hom_fg(R, M, N)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: N is a finitely generated R-module",
    "¬Q: Hom_R(M, N) is not a finitely generated R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2
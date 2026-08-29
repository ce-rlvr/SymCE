import sympy
from sympy.ntheory import primefactors
from sympy import S

# Top-level setup
Z = 0
Z1 = 1
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
QQ = S.Rationals
ZZ = S.Integers

def num_maximal_ideals(R):
    if isinstance(R, str):
        if R == "QQ": return 1
        if R == "ZZ": return float('inf')
        if R == "Z": return float('inf')
        if R.startswith("Z"):
            try:
                R = int(R[1:])
            except ValueError:
                pass
                
    if isinstance(R, int):
        if R == 1:
            return 0
        if R == 0:
            return float('inf')
        return len(primefactors(R))
        
    if R in [QQ, S.Rationals]:
        return 1
    if R in [ZZ, S.Integers]:
        return float('inf')
        
    raise ValueError(f"Unknown ring: {R}")

def is_nonzero_commutative(R):
    if isinstance(R, str):
        if R in ["QQ", "ZZ", "Z"]: return True
        if R.startswith("Z"):
            try:
                R = int(R[1:])
            except ValueError:
                pass
                
    if isinstance(R, int):
        return R != 1
        
    if R in [QQ, S.Rationals, ZZ, S.Integers]:
        return True
        
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        R1, R2 = witness
    except Exception:
        return [False, False]
        
    try:
        h1_ok = bool(is_nonzero_commutative(R2))
    except Exception:
        h1_ok = False
        
    try:
        # R1 x R2 is local iff the sum of the number of their maximal ideals is exactly 1
        neg_q_ok = bool((num_maximal_ideals(R1) + num_maximal_ideals(R2)) == 1)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    r"H_1: R_2 is a non-zero commutative ring",
    r"¬Q: The direct product ring R_1 \times R_2 is a local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1
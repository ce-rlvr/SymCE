import sympy
from sympy import ZZ, QQ
import math
import itertools
import functools

# Top-level setup
Z = ZZ
Q = QQ

def parse_witness(witness):
    R, S, E = None, None, None
    if isinstance(witness, str):
        parts = witness.split(',')
        for part in parts:
            if '=' in part:
                k, v = part.split('=', 1)
                k = k.strip().upper()
                v = v.strip()
                if k == 'R': R = v
                elif k == 'S': S = v
                elif k == 'E': E = v
    elif isinstance(witness, dict):
        R = witness.get("R", witness.get("r"))
        S = witness.get("S", witness.get("s"))
        E = witness.get("E", witness.get("e"))
    elif isinstance(witness, (tuple, list)) and len(witness) == 3:
        R, S, E = witness
    else:
        R = getattr(witness, "R", getattr(witness, "r", None))
        S = getattr(witness, "S", getattr(witness, "s", None))
        E = getattr(witness, "E", getattr(witness, "e", None))
        
    def norm_R(r):
        if r is None: return None
        s = str(r).strip()
        if s in ("ZZ", "Z", "Integers", "S.Integers", "Ring.Z"): return "Z"
        if s in ("QQ", "Q", "Rationals", "S.Rationals", "Field.Q"): return "Q"
        if s in ("k[x]", "F[x]", "Q[x]", "R[x]", "C[x]", "Z[x]"): return "k[x]"
        return s
        
    def norm_S(s):
        if s is None: return None
        st = str(s).strip().replace(" ", "")
        if st in ("{1}", "[1]", "(1,)", "1", "Set(1)"): return "{1}"
        if st in ("Z\\{0}", "ZZ\\{0}", "Z-{0}", "ZZ-{0}", "Z\\0", "ZZ\\0"): return "Z\\{0}"
        if st in ("k[x]\\{0}", "F[x]\\{0}", "Q[x]\\{0}"): return "k[x]\\{0}"
        return st
        
    def norm_E(e):
        if e is None: return None
        s = str(e).strip().replace(" ", "")
        if s in ("ZZ", "Z", "Integers", "S.Integers", "Module.Z"): return "Z"
        if s in ("QQ", "Q", "Rationals", "S.Rationals", "Module.Q"): return "Q"
        if s in ("Z/2Z", "Z2", "GF(2)", "F2"): return "Z/2Z"
        if s in ("k[x]", "F[x]", "Q[x]", "R[x]", "C[x]", "Z[x]"): return "k[x]"
        return s
        
    return norm_R(R), norm_S(S), norm_E(E)

def conditions(witness) -> list[bool]:
    R, S, E = parse_witness(witness)
    
    # H1: R is a commutative ring with identity
    try:
        h1 = (R in ["Z", "Q", "k[x]", "R", "C"])
    except Exception:
        h1 = False
        
    # H2: R is a Noetherian ring
    try:
        h2 = (R in ["Z", "Q", "k[x]", "R", "C"])
    except Exception:
        h2 = False
        
    # H3: S is a multiplicatively closed subset of R
    try:
        if R == "Z":
            h3 = (S in ["{1}", "Z\\{0}"])
        elif R in ["Q", "R", "C"]:
            h3 = (S in ["{1}", R + "\\{0}"])
        elif R == "k[x]":
            h3 = (S in ["{1}", "k[x]\\{0}"])
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: S^{-1}E is NOT an injective S^{-1}R-module
    try:
        if S == "{1}":
            S_inv_R = R
            S_inv_E = E
        elif S == "Z\\{0}" and R == "Z":
            S_inv_R = "Q"
            if E == "Z":
                S_inv_E = "Q"
            elif E == "Z/2Z":
                S_inv_E = "0"
            elif E == "Q":
                S_inv_E = "Q"
            else:
                S_inv_E = None
        elif S == "k[x]\\{0}" and R == "k[x]":
            S_inv_R = "k(x)"
            if E == "k[x]":
                S_inv_E = "k(x)"
            else:
                S_inv_E = None
        else:
            S_inv_R = None
            S_inv_E = None
            
        if S_inv_R is None or S_inv_E is None:
            neg_q = False
        else:
            is_injective = False
            if S_inv_R == "Q" and S_inv_E in ["Q", "0"]:
                is_injective = True
            elif S_inv_R == "Z" and S_inv_E == "Q":
                is_injective = True
            elif S_inv_R == "Z" and S_inv_E in ["Z", "Z/2Z"]:
                is_injective = False
            elif S_inv_R == "k[x]" and S_inv_E == "k[x]":
                is_injective = False
            elif S_inv_R == "k(x)" and S_inv_E == "k(x)":
                is_injective = True
            else:
                is_injective = True # default to True to avoid false positives
                
            neg_q = not is_injective
            
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}E is not an injective S^{-1}R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3
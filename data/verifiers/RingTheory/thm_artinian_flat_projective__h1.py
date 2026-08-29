import sympy
from sympy import S

Q = S.Rationals
Z = S.Integers
R = S.Reals
C = S.Complexes

Q_over_Z = (Q, Z)
Z_over_Z = (Z, Z)
R_over_Z = (R, Z)
Q_over_Q = (Q, Q)
R_over_R = (R, R)

def conditions(witness):
    try:
        if isinstance(witness, str):
            if witness == "Q_over_Z":
                witness = (S.Rationals, S.Integers)
            elif witness == "Z_over_Z":
                witness = (S.Integers, S.Integers)
            elif witness == "R_over_Z":
                witness = (S.Reals, S.Integers)
            elif witness == "Q_over_Q":
                witness = (S.Rationals, S.Rationals)
            elif witness == "R_over_R":
                witness = (S.Reals, S.Reals)
            else:
                parts = witness.split("_over_")
                if len(parts) == 2:
                    witness = (parts[0], parts[1])
                else:
                    return [False, False]
                    
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        M, R_ring = witness
    except Exception:
        return [False, False]
        
    h1 = False
    neg_q = False
    
    try:
        if M == R_ring:
            h1 = True
        elif M in (S.Rationals, S.Reals, S.Complexes) and R_ring == S.Integers:
            h1 = True
        elif isinstance(M, str) and R_ring == S.Integers:
            if M in ["Q", "R", "C", "Z[1/p]", "Z_{(p)}", "Z^N", "Baer-Specker"]:
                h1 = True
        elif isinstance(M, str) and isinstance(R_ring, str):
            if (M, R_ring) in [("Q", "Z"), ("R", "Z"), ("C", "Z"), ("Z[1/p]", "Z"), ("Z^N", "Z"), ("Baer-Specker", "Z")]:
                h1 = True
    except Exception:
        pass

    try:
        if M == R_ring:
            neg_q = False
        elif M in (S.Rationals, S.Reals, S.Complexes) and R_ring == S.Integers:
            neg_q = True
        elif isinstance(M, str) and R_ring == S.Integers:
            if M in ["Q", "R", "C", "Z[1/p]", "Z_{(p)}", "Z2", "Q/Z", "Z^N", "Baer-Specker"]:
                neg_q = True
            elif M == "Z":
                neg_q = False
        elif isinstance(M, str) and isinstance(R_ring, str):
            if (M, R_ring) in [("Q", "Z"), ("R", "Z"), ("C", "Z"), ("Z[1/p]", "Z"), ("Z2", "Z"), ("Q/Z", "Z"), ("Z^N", "Z"), ("Baer-Specker", "Z")]:
                neg_q = True
            elif (M, R_ring) in [("Z", "Z"), ("Q", "Q"), ("R", "R")]:
                neg_q = False
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a flat right R-module",
    "¬Q: M is not a projective right R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1
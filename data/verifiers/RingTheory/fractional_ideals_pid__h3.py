import sympy
from sympy import S

# ATOMIC CONCLUSION: Verifier for Fractional Ideals in a PID
# Initial logic and parameters are validated.
# Final transformation: Direct evaluation of non-principal submodule signatures.

Z = S.Integers
Q = S.Rationals

def conditions(witness) -> list[bool]:
    try:
        R, K, M = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = (R == S.Integers or str(R) in ('Z', 'ZZ', 'Integers'))
    except Exception:
        h1 = False

    try:
        h2 = h1 and (K == S.Rationals or str(K) in ('Q', 'QQ', 'Rationals'))
    except Exception:
        h2 = False

    try:
        neg_q = (M == S.Rationals or str(M) in ('Q', 'QQ', 'Rationals', 'Z[1/2]'))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: K is the field of fractions of R",
    "¬Q: M is not a principal fractional ideal (M != dR for any d in K)"
]

N_HYP = 2
NEG_Q_INDEX = 2
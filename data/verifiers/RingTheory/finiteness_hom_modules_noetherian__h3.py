import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
# The witness should be a tuple (R, M, N) representing the ring R, and modules M, N.
# For example, (ZZ, ZZ, QQ) represents R=Z, M=Z, N=Q.

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
        R, M, N = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative Noetherian ring
    try:
        h1 = False
        if R in [ZZ, QQ]:
            h1 = True
        elif isinstance(R, str) and R in ['ZZ', 'QQ', 'Z', 'Q']:
            h1 = True
        elif hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
            h1 = True
    except Exception:
        h1 = False

    # H_2: M is a finitely generated R-module
    try:
        h2 = False
        if M == R:
            h2 = True
        elif isinstance(M, str) and isinstance(R, str) and M == R:
            h2 = True
        elif isinstance(M, str) and R == ZZ and M in ['ZZ', 'Z']:
            h2 = True
        elif isinstance(M, str) and R == QQ and M in ['QQ', 'Q']:
            h2 = True
        elif isinstance(M, tuple) and len(M) >= 2 and M[0] == 'free' and M[1] == R:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: Hom_R(M, N) is not a finitely generated R-module
    try:
        neg_q = False
        is_M_eq_R = (M == R) or (isinstance(M, str) and isinstance(R, str) and M == R) or (R == ZZ and M in ['ZZ', 'Z']) or (R == QQ and M in ['QQ', 'Q'])
        if is_M_eq_R:
            # Hom_R(R, N) is isomorphic to N.
            # We check if N is NOT finitely generated over R.
            if (R == ZZ or R in ['ZZ', 'Z']) and (N == QQ or N in ['QQ', 'Q', 'Q/Z']):
                neg_q = True
            elif hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
                if hasattr(N, 'is_FractionField') and N.is_FractionField:
                    neg_q = True
                elif N == 'fraction_field':
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: M is a finitely generated R-module",
    "¬Q: Hom_R(M, N) is not a finitely generated R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2
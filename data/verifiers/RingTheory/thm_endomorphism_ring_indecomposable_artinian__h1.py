import sympy
from sympy import S
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x

# Top-level setup
Z = ZZ
Q = QQ
Integers = S.Integers
Rationals = S.Rationals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If M is a finitely generated indecomposable right R-module, 
    then End_R(M) is a local ring."
    (The dropped hypothesis was that R is an Artinian ring).
    """
    h1 = False
    neg_q = False
    
    try:
        # The witness could be provided as a tuple (R, M) or just M (assuming R=M).
        if isinstance(witness, tuple) and len(witness) == 2:
            M = witness[1]
        else:
            M = witness
            
        s = str(M).strip()
        
        # Z is a finitely generated indecomposable Z-module.
        # End_Z(Z) is isomorphic to Z, which is not a local ring (it has infinitely many maximal ideals).
        if M == ZZ or M == S.Integers or M is int or s in ["Z", "ZZ", "Integers", "S.Integers", "Integers()", "<class 'int'>"]:
            h1 = True
            neg_q = True
            
        # Q is a finitely generated indecomposable Q-module.
        # End_Q(Q) is isomorphic to Q, which is a field, hence a local ring.
        elif M == QQ or M == S.Rationals or M is float or s in ["Q", "QQ", "Rationals", "S.Rationals", "Rationals()", "<class 'float'>"]:
            h1 = True
            neg_q = False
            
        # Polynomial rings over fields or domains (e.g., Z[x], Q[x]) are integral domains,
        # hence indecomposable as modules over themselves.
        # Their endomorphism rings are themselves, which are not local rings.
        elif hasattr(M, 'is_Poly') or 'Poly' in s or s in ["Z[x]", "Q[x]", "R[x]", "C[x]", "ZZ[x]", "QQ[x]", "k[x]", "F[x]"]:
            h1 = True
            neg_q = True
            
        # Finite rings Z/nZ
        elif isinstance(M, int) and M > 1:
            from sympy.ntheory import factorint
            f = factorint(M)
            if len(f) == 1:
                # n = p^k: indecomposable and local
                h1 = True
                neg_q = False
            else:
                # n has multiple prime factors: decomposes by Chinese Remainder Theorem, and not local
                h1 = False
                neg_q = True
                
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a finitely generated indecomposable right R-module",
    "¬Q: The endomorphism ring End_R(M) is not a local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1
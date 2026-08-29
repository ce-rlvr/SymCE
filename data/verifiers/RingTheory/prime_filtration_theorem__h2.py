import sympy
from sympy import abc

ZZ = sympy.S.Integers
QQ = sympy.S.Rationals
RR = sympy.S.Reals
CC = sympy.S.Complexes
x = abc.x
y = abc.y
z = abc.z

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            R, M = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H1: R is a commutative Noetherian ring
    h1 = False
    try:
        if R in (ZZ, QQ, RR, CC):
            h1 = True
        elif hasattr(R, 'is_PolyRing') or hasattr(R, 'is_PolynomialRing'):
            domain = getattr(R, 'domain', None)
            if domain in (ZZ, QQ, RR, CC):
                h1 = True
        elif isinstance(R, str):
            R_str = R.replace(" ", "").lower()
            if R_str in ['z', 'q', 'r', 'c', 'zz', 'qq', 'rr', 'cc']:
                h1 = True
            elif R_str.startswith('z[') or R_str.startswith('q['):
                h1 = True
    except Exception:
        pass

    # neg_Q: M does not have a finite prime filtration
    # (This is true if M is not finitely generated over R)
    neg_q = False
    try:
        if R == ZZ and M in (QQ, RR, CC):
            neg_q = True
        elif R == QQ and M in (RR, CC):
            neg_q = True
        elif hasattr(M, 'is_PolyRing') or hasattr(M, 'is_PolynomialRing'):
            M_domain = getattr(M, 'domain', None)
            if M_domain == R:
                neg_q = True
            elif hasattr(R, 'is_PolyRing') and M_domain == getattr(R, 'domain', None):
                if len(getattr(M, 'gens', [])) > len(getattr(R, 'gens', [])):
                    neg_q = True
        elif hasattr(M, 'is_FracField'):
            if getattr(M, 'domain', None) == R and not getattr(R, 'is_Field', False):
                neg_q = True
        elif isinstance(M, str):
            M_str = M.replace(" ", "").lower()
            if R in (ZZ, 'Z', 'ZZ', 'z', 'zz') and M_str in ['q', 'r', 'c', 'qq', 'rr', 'cc', 'q/z', 'r/z']:
                neg_q = True
            elif 'infty' in M_str or 'infinity' in M_str or 'inf' in M_str:
                neg_q = True
            elif 'oplus' in M_str or 'bigoplus' in M_str:
                neg_q = True
            elif M_str.startswith(str(R).lower() + '[') or M_str.startswith(str(R).lower() + '('):
                neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: M does not have a finite prime filtration"
]

N_HYP = 1
NEG_Q_INDEX = 1
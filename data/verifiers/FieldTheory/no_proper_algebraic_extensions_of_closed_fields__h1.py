import sympy
from sympy import I, sqrt, Rational, Integer, S
from sympy.abc import x, y, z

QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    try:
        # The witness is expected to be a tuple (K, L) representing the base field and the extension field.
        # If a single domain is provided, we assume it is L and its base domain is K.
        if isinstance(witness, tuple) and len(witness) == 2:
            K, L = witness
        else:
            L = witness
            K = getattr(L, 'domain', sympy.QQ)
    except Exception:
        return [False, False, False]

    # H_1: Let L be an extension field of K.
    try:
        is_k_field = getattr(K, 'is_Field', False) or getattr(K, 'is_field', False) or K in (sympy.QQ, sympy.RR, sympy.CC, sympy.S.Reals, sympy.S.Complexes)
        is_l_field = getattr(L, 'is_Field', False) or getattr(L, 'is_field', False) or L in (sympy.QQ, sympy.RR, sympy.CC, sympy.S.Reals, sympy.S.Complexes)
        is_fields = is_k_field and is_l_field
        
        is_ext = False
        if K == L:
            is_ext = True
        elif K == sympy.QQ and hasattr(L, 'domain') and L.domain == sympy.QQ:
            is_ext = True
        elif K in (sympy.RR, sympy.S.Reals) and L in (sympy.CC, sympy.S.Complexes):
            is_ext = True
        else:
            try:
                is_ext = (K.unify(L) == L)
            except Exception:
                is_ext = False
                
        h1 = bool(is_fields and is_ext)
    except Exception:
        h1 = False

    # H_2: L is an algebraic extension of K.
    try:
        if not h1:
            h2 = False
        elif L == K:
            h2 = True
        elif hasattr(L, 'ext') and hasattr(L, 'domain'):
            # In SymPy, AlgebraicField objects have an 'ext' attribute and are algebraic over their domain.
            h2 = True
        elif K in (sympy.RR, sympy.S.Reals) and L in (sympy.CC, sympy.S.Complexes):
            # The complex numbers are an algebraic extension of the real numbers (degree 2).
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: L is not equal to K.
    try:
        neg_q = bool(L != K)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L is an extension field of K",
    "H_2: L is an algebraic extension of K",
    "¬Q: L is not equal to K"
]

N_HYP = 2
NEG_Q_INDEX = 2
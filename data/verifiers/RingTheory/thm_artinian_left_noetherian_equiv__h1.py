import sympy
from sympy import ZZ, QQ

# Top-level setup
Z = ZZ
Q = QQ

def is_left_artinian(witness):
    if witness in (sympy.ZZ, sympy.S.Integers):
        return False
    if witness in (sympy.QQ, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
        return True
    if hasattr(witness, 'is_left_artinian'):
        val = witness.is_left_artinian
        return val() if callable(val) else val
    if type(witness).__name__ == 'PolyRing':
        return False
    if isinstance(witness, str):
        w = witness.strip().lower()
        if w in ['z', 'zz', 'integers']:
            return False
        if w in ['q', 'qq', 'rationals', 'r', 'reals', 'c', 'complexes']:
            return True
    raise ValueError("Cannot determine if left Artinian")

def is_left_noetherian(witness):
    if witness in (sympy.ZZ, sympy.S.Integers):
        return True
    if witness in (sympy.QQ, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
        return True
    if hasattr(witness, 'is_left_noetherian'):
        val = witness.is_left_noetherian
        return val() if callable(val) else val
    if type(witness).__name__ == 'PolyRing':
        if hasattr(witness, 'domain') and hasattr(witness, 'gens'):
            if (witness.domain.is_Field or witness.domain == sympy.ZZ) and len(witness.gens) < float('inf'):
                return True
        return False
    if isinstance(witness, str):
        w = witness.strip().lower()
        if w in ['z', 'zz', 'integers']:
            return True
        if w in ['q', 'qq', 'rationals', 'r', 'reals', 'c', 'complexes']:
            return True
    raise ValueError("Cannot determine if left Noetherian")

def conditions(witness) -> list[bool]:
    try:
        art = bool(is_left_artinian(witness))
        noe = bool(is_left_noetherian(witness))
        neg_q = (art != noe)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is left Artinian if and only if R is left Noetherian is FALSE"
]

N_HYP = 0
NEG_Q_INDEX = 0
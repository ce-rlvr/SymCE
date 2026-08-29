import sympy
from sympy import QQ, RR, CC, ZZ, I, sqrt, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# We provide standard domains that might be used in the witness.
# The witness should be a tuple (L, K, S) where L and K are SymPy domains representing fields, 
# and S is a subset/domain.

def conditions(witness) -> list[bool]:
    try:
        # Witness must be a tuple of (L, K, S)
        if len(witness) != 3:
            return [False, False]
        L, K, S = witness
    except Exception:
        return [False, False]
        
    # H_1: L/K is a field extension
    try:
        L_is_field = getattr(L, 'is_Field', False)
        K_is_field = getattr(K, 'is_Field', False)
        if L_is_field and K_is_field:
            # K is a subfield of L if they are the same or K can be unified into L
            h1 = (K == L) or (K.unify(L) == L)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # neg_Q: S is not a subfield of L
    try:
        S_is_field = getattr(S, 'is_Field', False)
        if S_is_field:
            # S is a subfield of L if it is a field and is contained in L
            S_is_subfield = (S == L) or (S.unify(L) == L)
        else:
            S_is_subfield = False
        neg_q = not S_is_subfield
    except Exception:
        # If S doesn't support unify or isn't a field, it's not a subfield.
        neg_q = True
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: L/K is a field extension",
    "¬Q: S is not a subfield of L"
]

N_HYP = 1
NEG_Q_INDEX = 1
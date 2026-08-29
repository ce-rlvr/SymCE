import sympy
from sympy import RR, CC, QQ, S

# Top-level setup for potential witness expressions
Reals = S.Reals
Complexes = S.Complexes
Rationals = S.Rationals
QQbar = sympy.Symbol('QQbar')

def get_field_name(K):
    """Normalize the string representation of common fields."""
    s = str(K)
    if s in ['RR', 'Reals', 'S.Reals', 'ℝ']: 
        return 'RR'
    if s in ['CC', 'Complexes', 'S.Complexes', 'ℂ']: 
        return 'CC'
    if s in ['QQ', 'Rationals', 'S.Rationals', 'ℚ']: 
        return 'QQ'
    if s == 'QQbar': 
        return 'QQbar'
    return s

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (F, K1, K2), check the remaining hypotheses and the negated conclusion.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        F, K1, K2 = witness
    except Exception:
        return [False, False, False]

    # H_1: F is a field
    try:
        h1 = False
        f_name = get_field_name(F)
        if f_name in ['RR', 'CC', 'QQ']:
            h1 = True
        elif hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif hasattr(F, 'is_field') and F.is_field:
            h1 = True
    except Exception:
        h1 = False

    # H_2: K1 is an algebraic closure of F
    try:
        h2 = False
        f_name = get_field_name(F)
        k1_name = get_field_name(K1)
        if f_name == 'RR' and k1_name == 'CC':
            h2 = True
        elif f_name == 'CC' and k1_name == 'CC':
            h2 = True
        elif f_name == 'QQ' and k1_name == 'QQbar':
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: There does not exist a field isomorphism from K1 to K2 that fixes every element of F.
    # For the standard fields we support, they are isomorphic over F iff they are the same field.
    try:
        k1_name = get_field_name(K1)
        k2_name = get_field_name(K2)
        neg_q = (k1_name != k2_name)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K1 is an algebraic closure of F",
    "¬Q: There does not exist a field isomorphism from K1 to K2 that fixes every element of F"
]

N_HYP = 2
NEG_Q_INDEX = 2
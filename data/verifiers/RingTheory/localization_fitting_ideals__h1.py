import sympy
from sympy import symbols

# Top-level setup
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    neg_q = False

    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            h1, h2, h3, commutes = witness
            return [bool(h1), bool(h2), bool(h3), not bool(commutes)]
    except Exception:
        pass

    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('M_is_finitely_presented', False))
            h2 = bool(witness.get('S_is_multiplicatively_closed', False))
            h3 = bool(witness.get('k_is_non_negative', False))
            neg_q = not bool(witness.get('localization_commutes', True))
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        h1 = bool(getattr(witness, 'M_is_finitely_presented', False))
        h2 = bool(getattr(witness, 'S_is_multiplicatively_closed', False))
        h3 = bool(getattr(witness, 'k_is_non_negative', False))
        neg_q = not bool(getattr(witness, 'localization_commutes', True))
        return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: M is a finitely presented R-module",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: k is a non-negative integer",
    "¬Q: Fitt_k(S^{-1}M) != S^{-1}Fitt_k(M)"
]

N_HYP = 3
NEG_Q_INDEX = 3
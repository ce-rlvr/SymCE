import sympy
from sympy import GF, QQ, ZZ
from sympy.abc import x, y, t

# Setup named objects for potential witnesses
F2 = GF(2)
F3 = GF(3)
F5 = GF(5)

def is_perfect(K):
    """
    Checks if a SymPy domain is a perfect field.
    """
    try:
        if not getattr(K, 'is_Field', False):
            return False
        char = getattr(K, 'characteristic', 0)
        if char == 0:
            return True
        if getattr(K, 'is_FiniteField', False):
            return True
        # In characteristic p > 0, a fraction field (like F_p(x)) is not perfect.
        if char > 0 and type(K).__name__ == 'FractionField':
            return False
        return True
    except Exception:
        return False

def is_subfield(sub, sup):
    """
    Checks if `sub` is a subfield of `sup` using SymPy domains.
    """
    if sub == sup:
        return True
    try:
        if sup.unify(sub) == sup:
            return True
    except Exception:
        pass
    # Fallback check for fraction fields
    try:
        if hasattr(sup, 'domain'):
            if sub == sup.domain:
                return True
            if hasattr(sup.domain, 'domain') and sub == sup.domain.domain:
                return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            K = witness.get('K')
            E = witness.get('E')
        elif isinstance(witness, (list, tuple)) and len(witness) >= 3:
            F = witness[0]
            K = witness[1]
            E = witness[2]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: F is a perfect field
    try:
        h1 = getattr(F, 'is_Field', False) and is_perfect(F)
    except Exception:
        h1 = False

    # H_2: K is a field such that F \subseteq K \subseteq E
    try:
        h2 = (getattr(K, 'is_Field', False) and 
              getattr(E, 'is_Field', False) and 
              is_subfield(F, K) and 
              is_subfield(K, E))
    except Exception:
        h2 = False

    # ¬Q: K is not a perfect field
    try:
        neg_q = getattr(K, 'is_Field', False) and not is_perfect(K)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a perfect field",
    "H_2: K is a field such that F \\subseteq K \\subseteq E",
    "¬Q: K is not a perfect field"
]

N_HYP = 2
NEG_Q_INDEX = 2
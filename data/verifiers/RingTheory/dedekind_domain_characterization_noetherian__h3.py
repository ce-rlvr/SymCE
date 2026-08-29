import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def is_noetherian(domain):
    if not hasattr(domain, 'is_Field'):
        return False
    if domain.is_Field:
        return True
    if domain == ZZ:
        return True
    if hasattr(domain, 'domain') and hasattr(domain, 'symbols'):
        return is_noetherian(domain.domain)
    return False

def is_integrally_closed(domain):
    if not hasattr(domain, 'is_Field'):
        return False
    if domain.is_Field:
        return True
    if domain == ZZ:
        return True
    if hasattr(domain, 'domain') and hasattr(domain, 'symbols'):
        return is_integrally_closed(domain.domain)
    return False

def krull_dimension(domain):
    if not hasattr(domain, 'is_Field'):
        return None
    if domain.is_Field:
        return 0
    if domain == ZZ:
        return 1
    if hasattr(domain, 'domain') and hasattr(domain, 'symbols'):
        base_dim = krull_dimension(domain.domain)
        if base_dim is None:
            return None
        return base_dim + len(domain.symbols)
    return None

def is_dedekind(domain):
    if not is_noetherian(domain):
        return False
    if not is_integrally_closed(domain):
        return False
    dim = krull_dimension(domain)
    if dim is None:
        return False
    return dim <= 1

def conditions(witness):
    try:
        h1 = is_noetherian(witness)
    except Exception:
        h1 = False

    try:
        h2 = is_integrally_closed(witness)
    except Exception:
        h2 = False

    try:
        if not hasattr(witness, 'is_Field'):
            neg_q = False
        else:
            neg_q = not is_dedekind(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian integral domain",
    "H_2: R is integrally closed in its field of fractions",
    "¬Q: R is not a Dedekind domain"
]

N_HYP = 2
NEG_Q_INDEX = 2
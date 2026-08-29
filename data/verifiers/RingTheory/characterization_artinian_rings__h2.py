import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.polys.domains.domain import Domain
from sympy.abc import x, y, z

def is_noetherian(D, visited=None):
    if visited is None:
        visited = set()
    if D in visited:
        return False
    visited.add(D)
    if getattr(D, 'is_Field', False):
        return True
    if D == ZZ:
        return True
    if hasattr(D, 'domain') and hasattr(D, 'gens'):
        return is_noetherian(D.domain, visited)
    return False

def is_artinian(D):
    if getattr(D, 'is_Field', False):
        return True
    if D == ZZ:
        return False
    if hasattr(D, 'domain') and hasattr(D, 'gens'):
        return False
    return False

def conditions(witness):
    try:
        h1_ok = bool(isinstance(witness, Domain) and is_noetherian(witness))
    except Exception:
        h1_ok = False

    try:
        if not isinstance(witness, Domain):
            neg_q_ok = False
        else:
            neg_q_ok = not is_artinian(witness)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: R is not an Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1
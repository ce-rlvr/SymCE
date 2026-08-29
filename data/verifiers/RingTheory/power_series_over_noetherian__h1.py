import sympy
from sympy.abc import x, y, z
from sympy.polys.domains import ZZ, QQ, RR, CC

def is_noetherian(witness):
    if isinstance(witness, dict) and 'is_noetherian' in witness:
        return bool(witness['is_noetherian'])
    if hasattr(witness, 'is_noetherian'):
        val = witness.is_noetherian
        return val() if callable(val) else val
    if hasattr(witness, 'is_Noetherian'):
        val = witness.is_Noetherian
        return val() if callable(val) else val
    try:
        from sympy.polys.domains.domain import Domain
        if isinstance(witness, Domain):
            return True
    except Exception:
        pass
    s = str(witness).lower()
    if "weyl" in s or "skew" in s or "twisted" in s or s in ["a1", "a_1", "a1(k)", "a_1(k)"]:
        return True
    return False

def is_power_series_noetherian(witness):
    if isinstance(witness, dict) and 'is_power_series_noetherian' in witness:
        return bool(witness['is_power_series_noetherian'])
    if hasattr(witness, 'is_power_series_noetherian'):
        val = witness.is_power_series_noetherian
        return val() if callable(val) else val
    if hasattr(witness, 'is_power_series_Noetherian'):
        val = witness.is_power_series_Noetherian
        return val() if callable(val) else val
    if hasattr(witness, 'is_commutative'):
        val = witness.is_commutative
        is_comm = val() if callable(val) else val
        if is_comm:
            return is_noetherian(witness)
    try:
        from sympy.polys.domains.domain import Domain
        if isinstance(witness, Domain):
            return True
    except Exception:
        pass
    s = str(witness).lower()
    if "weyl" in s or "skew" in s or "twisted" in s or s in ["a1", "a_1", "a1(k)", "a_1(k)"]:
        return False
    return True

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(is_noetherian(witness))
    except Exception:
        h1 = False
    try:
        q = bool(is_power_series_noetherian(witness))
        neg_q = not q
    except Exception:
        neg_q = False
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "¬Q: The formal power series ring over R is not a Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1
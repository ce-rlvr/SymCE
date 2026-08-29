import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: The Krull dimension of R is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        def is_euclidean_domain(R):
            if getattr(R, 'is_Field', False):
                return True
            if R == ZZ:
                return True
            if hasattr(R, 'domain') and hasattr(R, 'symbols'):
                if getattr(R.domain, 'is_Field', False) and len(R.symbols) == 1:
                    return True
            return False
        h1 = bool(is_euclidean_domain(witness))
    except Exception:
        h1 = False

    try:
        def krull_dimension(R):
            if getattr(R, 'is_Field', False):
                return 0
            if R == ZZ:
                return 1
            if hasattr(R, 'domain') and hasattr(R, 'symbols'):
                base_dim = krull_dimension(R.domain)
                if base_dim is not None:
                    return base_dim + len(R.symbols)
            return None
        
        dim = krull_dimension(witness)
        if dim is not None:
            neg_q = bool(dim != 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]
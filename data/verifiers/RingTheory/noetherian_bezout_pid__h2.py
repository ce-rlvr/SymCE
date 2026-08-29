import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.polys.domains.domain import Domain

def conditions(witness):
    # H_1: R is an integral domain
    try:
        # In SymPy, all Domain objects represent integral domains (or fields).
        h1 = isinstance(witness, Domain)
    except Exception:
        h1 = False

    # H_2: R is a Noetherian ring
    try:
        def check_noetherian(ring):
            if ring in (sympy.ZZ, sympy.QQ):
                return True
            if getattr(ring, 'is_Field', False):
                return True
            if hasattr(ring, 'domain') and ring.domain is not ring:
                # Polynomial rings and fraction fields over a Noetherian ring are Noetherian
                return check_noetherian(ring.domain)
            return False
        
        h2 = check_noetherian(witness)
    except Exception:
        h2 = False

    # ¬Q: R is not a principal ideal domain
    try:
        if hasattr(witness, 'is_PID') and witness.is_PID is not None:
            is_pid = bool(witness.is_PID)
        else:
            # Fallback logic for PID check
            if getattr(witness, 'is_Field', False):
                is_pid = True
            elif witness == sympy.ZZ:
                is_pid = True
            elif hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
                # A polynomial ring is a PID iff it is in one variable over a field
                is_pid = (len(witness.symbols) == 1) and getattr(witness.domain, 'is_Field', False)
            else:
                is_pid = False
                
        neg_q = not is_pid
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: R is a Noetherian ring",
    "¬Q: R is not a principal ideal domain"
]

N_HYP = 2
NEG_Q_INDEX = 2
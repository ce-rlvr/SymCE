import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y

# Top-level setup: named object bindings that the witness expression may reference.
ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)
QQ_x_y = QQ.poly_ring(x, y)
ZZ_x_y = ZZ.poly_ring(x, y)

def conditions(witness) -> list[bool]:
    try:
        if not hasattr(witness, 'is_UFD') or not hasattr(witness, 'is_PID'):
            return [False]
        
        is_ufd = witness.is_UFD
        is_pid = witness.is_PID
        
        if is_ufd is None or is_pid is None:
            return [False]
            
        # The conclusion is "R is a UFD iff R is a PID".
        # The negated conclusion is that this equivalence fails.
        neg_q = bool(is_ufd) != bool(is_pid)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is a UFD but not a PID (or vice versa)"
]

N_HYP = 0
NEG_Q_INDEX = 0
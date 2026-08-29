import sympy
from sympy import ZZ, QQ
from sympy.abc import x

# Standard ring domains that might be used as witnesses
Qx = QQ.poly_ring(x)
Zx = ZZ.poly_ring(x)

def conditions(witness):
    try:
        # The witness must be a ring domain with these properties
        if not hasattr(witness, 'is_PID') or not hasattr(witness, 'is_Field'):
            return [False]
            
        lhs = (witness.is_PID is True)
        is_field = (witness.is_Field is True)
        
        # Sympy domains do not natively represent Discrete Valuation Rings (DVRs).
        # A DVR is a local PID that is not a field. Standard domains like ZZ and K[x] are not DVRs.
        # We allow the witness to explicitly declare itself as a DVR if it's a custom object.
        if hasattr(witness, 'is_DVR'):
            is_dvr = (witness.is_DVR is True)
        else:
            is_dvr = False
            
        rhs = is_field or is_dvr
        
        # The conjecture states: R is a PID <=> R is a field or a DVR.
        # The negation is True when this equivalence fails.
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is a PID but neither a field nor a DVR, or R is a field/DVR but not a PID"
]

N_HYP = 0
NEG_Q_INDEX = 0
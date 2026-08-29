import sympy
from sympy.abc import x, y, z, t
from sympy.polys.domains import QQ, ZZ, GF, RR, CC

def conditions(witness):
    try:
        is_field = getattr(witness, 'is_Field', False)
        if not is_field:
            is_perf = False
        else:
            char = getattr(witness, 'characteristic', 0)
            if char == 0:
                is_perf = True
            else:
                is_finite = getattr(witness, 'is_FiniteField', False) or ('FiniteField' in witness.__class__.__name__)
                if is_finite:
                    is_perf = True
                else:
                    is_perf = False
    except Exception:
        is_perf = False

    neg_q = not is_perf
    return [bool(neg_q)]

CONDITION_LABELS = ["¬Q: K is not a perfect field"]
N_HYP = 0
NEG_Q_INDEX = 0
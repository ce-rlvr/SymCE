import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness satisfies the negated conclusion.
    The conclusion states that there exists a unique minimal Euclidean function on R.
    This is true if and only if R is a Euclidean domain.
    Therefore, the negated conclusion is true iff R is NOT a Euclidean domain.
    """
    try:
        is_euclid = False
        
        if witness == sympy.ZZ or witness == sympy.S.Integers:
            is_euclid = True
        elif witness in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            is_euclid = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            is_euclid = True
        elif hasattr(witness, 'is_PID') and witness.is_PID is not None:
            # In SymPy, domains like QQ[x] have is_PID=True, while ZZ[x] and QQ[x,y] have is_PID=False.
            # All Euclidean domains are PIDs. For the standard SymPy domains, PID implies Euclidean.
            is_euclid = bool(witness.is_PID)
        elif hasattr(witness, 'symbols') and hasattr(witness, 'dom'):
            # Fallback for polynomial rings
            if len(witness.symbols) == 1 and hasattr(witness.dom, 'is_Field') and witness.dom.is_Field:
                is_euclid = True
            else:
                is_euclid = False
        else:
            is_euclid = False
            
        neg_q = not is_euclid
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R does not have a unique minimal Euclidean function"
]

N_HYP = 0
NEG_Q_INDEX = 0
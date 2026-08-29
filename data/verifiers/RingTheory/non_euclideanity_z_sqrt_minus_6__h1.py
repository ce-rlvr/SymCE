import sympy
from sympy import Symbol
from sympy.polys.domains import ZZ, QQ

x = Symbol('x')
Z = ZZ
Q = QQ

def conditions(witness) -> list[bool]:
    try:
        if getattr(witness, 'is_Field', False):
            neg_q = True
        elif witness == ZZ:
            neg_q = True
        elif hasattr(witness, 'domain') and getattr(witness.domain, 'is_Field', False) and hasattr(witness, 'gens') and len(witness.gens) == 1:
            neg_q = True
        elif getattr(witness, 'is_PID', False):
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = ["¬Q: R is a Euclidean domain"]
N_HYP = 0
NEG_Q_INDEX = 0
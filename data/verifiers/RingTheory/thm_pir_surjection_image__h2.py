import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.polys.domains.domain import Domain
from sympy.abc import x, y

# Top-level setup: named object bindings
ZZ_x = ZZ[x]
QQ_x = QQ[x]
QQ_x_y = QQ[x, y]
ZZ_x_y = ZZ[x, y]

def is_ring(domain):
    if isinstance(domain, Domain):
        return True
    if getattr(domain, 'is_Ring', False):
        return True
    return False

def is_pid(domain):
    is_pid_attr = getattr(domain, 'is_PID', None)
    if is_pid_attr is not None:
        return bool(is_pid_attr)
    
    if getattr(domain, 'is_Field', False):
        return True
    if domain.__class__.__name__ in ('IntegerRing', 'RationalField', 'RealField', 'ComplexField'):
        return True
    if hasattr(domain, 'dom') and hasattr(domain, 'gens'):
        if len(domain.gens) == 1 and getattr(domain.dom, 'is_Field', False):
            return True
        if len(domain.gens) == 1 and domain.dom.__class__.__name__ in ('RationalField', 'RealField', 'ComplexField'):
            return True
    return False

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (R, S) representing the two rings.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        R, S = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R and S are rings
    try:
        h1_ok = bool(is_ring(R) and is_ring(S))
    except Exception:
        h1_ok = False
        
    # H_2: R is a principal ideal ring
    try:
        h2_ok = bool(is_pid(R))
    except Exception:
        h2_ok = False
        
    # ¬Q: S is not a principal ideal ring
    try:
        neg_q_ok = not bool(is_pid(S))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: R is a principal ideal ring",
    "¬Q: S is not a principal ideal ring"
]

N_HYP = 2
NEG_Q_INDEX = 2
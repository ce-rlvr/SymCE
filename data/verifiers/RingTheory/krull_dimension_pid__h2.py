import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def conditions(witness):
    try:
        # H1: R is a principal ideal domain
        is_pid = False
        if getattr(witness, 'is_Field', False):
            is_pid = True
        elif getattr(witness, 'is_PID', False):
            is_pid = True
        elif witness == ZZ:
            is_pid = True
        elif hasattr(witness, 'dom') and hasattr(witness, 'gens'):
            if len(witness.gens) == 1 and getattr(witness.dom, 'is_Field', False):
                is_pid = True
        h1 = bool(is_pid)
    except Exception:
        h1 = False

    try:
        # Q: The Krull dimension of R is exactly 1.
        # ¬Q: The Krull dimension of R is NOT exactly 1.
        dim = None
        if getattr(witness, 'is_Field', False):
            dim = 0
        elif witness == ZZ:
            dim = 1
        elif hasattr(witness, 'dom') and hasattr(witness, 'gens'):
            if getattr(witness.dom, 'is_Field', False):
                dim = len(witness.gens)
            elif witness.dom == ZZ:
                dim = 1 + len(witness.gens)
        
        if dim is None:
            neg_q = False
        else:
            neg_q = bool(dim != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: The Krull dimension of R is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
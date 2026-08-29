import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y

# Pre-defined rings and modules for witness construction
ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (R, M) where R is a ring and M is an R-module.
    """
    try:
        # Witness must be a pair (Ring, Module)
        if len(witness) != 2:
            return [False, False]
        R, M = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a principal ideal domain
    try:
        # Normalize common SymPy sets to domains
        if R == sympy.S.Integers:
            R_dom = ZZ
        elif R == sympy.S.Rationals:
            R_dom = QQ
        else:
            R_dom = R
            
        h1 = bool(R_dom.is_PID)
    except Exception:
        h1 = False
        
    # ¬Q: M is NOT a finitely presented R-module
    try:
        is_fp = True
        
        # Normalize common SymPy sets to domains
        if M == sympy.S.Integers:
            M_dom = ZZ
        elif M == sympy.S.Rationals:
            M_dom = QQ
        else:
            M_dom = M
            
        # Check known cases of modules over R
        if R_dom == M_dom:
            # R over R is a free module of rank 1 (finitely presented)
            is_fp = True
        elif hasattr(M_dom, 'domain') and M_dom.domain == R_dom:
            # Polynomial ring R[x] over R has infinite rank (not finitely generated)
            is_fp = False
        elif hasattr(M_dom, 'ring') and M_dom.ring == R_dom and M_dom != R_dom:
            # Fraction field of R over R (e.g., QQ over ZZ) is not finitely generated
            is_fp = False
        elif hasattr(M_dom, 'get_ring') and M_dom.get_ring() == R_dom and M_dom != R_dom:
            # Fallback for fraction field check
            is_fp = False
        elif R_dom == ZZ and M_dom == QQ:
            # Explicit check for QQ over ZZ
            is_fp = False
        elif isinstance(M_dom, tuple) and all(m == R_dom for m in M_dom):
            # Finite direct sum R^n
            is_fp = True
        else:
            # Default to True (fails the counterexample check) to avoid false positives
            is_fp = True
            
        neg_q = not is_fp
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: M is not a finitely presented R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1
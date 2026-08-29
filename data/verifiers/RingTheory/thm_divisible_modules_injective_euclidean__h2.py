import sympy
from sympy import ZZ, QQ
from sympy.abc import x

# Top-level setup: named object bindings that the witness expression may reference
Z = ZZ
Q = QQ
Qx = QQ[x]
Zx = ZZ[x]

def is_euclidean_domain(R):
    """Check if R is a known Euclidean domain."""
    if R == ZZ:
        return True
    if R == QQ:
        return True
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        # A polynomial ring over a field in one variable is a Euclidean domain
        if R.domain.is_Field and len(R.symbols) == 1:
            return True
    try:
        from sympy import ZZ_I
        if R == ZZ_I:
            return True
    except ImportError:
        pass
    return False

def is_injective_module(R, M):
    """Check if M is an injective R-module."""
    # Over a field, every module is a vector space, hence injective
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
        
    # An integral domain is an injective module over itself if and only if it is a field
    if M == R:
        if hasattr(R, 'is_Field'):
            return R.is_Field
            
    # Specific cases for R = ZZ
    if R == ZZ:
        if M == QQ:
            return True
        if hasattr(M, 'is_FiniteField') and M.is_FiniteField:
            return False
            
    # Specific cases for Gaussian integers
    try:
        from sympy import ZZ_I, QQ_I
        if R == ZZ_I:
            if M == QQ_I:
                return True
    except ImportError:
        pass
        
    raise ValueError(f"Cannot determine if {M} is injective over {R}")

def conditions(witness) -> list[bool]:
    # Parse the witness. It can be a dict, a tuple (R, M), or just R (implying M = R).
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            M = witness.get('M')
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            R = witness
            M = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a Euclidean domain
    try:
        h1_ok = bool(is_euclidean_domain(R))
    except Exception:
        h1_ok = False
        
    # ¬Q: M is not an injective R-module
    try:
        neg_q_ok = not is_injective_module(R, M)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: M is not an injective R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1
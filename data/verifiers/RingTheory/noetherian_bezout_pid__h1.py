import sympy
import sympy.abc
from sympy import Symbol
from sympy.polys.domains import ZZ, QQ, RR, CC, EX

# Setup common symbols for polynomial rings
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
t = Symbol('t')

def is_PID(R):
    """Check if R is a Principal Ideal Domain."""
    if hasattr(R, 'is_PID'):
        return bool(R.is_PID)
    if hasattr(R, 'is_Field') and R.is_Field:
        return True
    if R == ZZ:
        return True
    return False

def is_Noetherian(R):
    """Check if R is a Noetherian ring."""
    if hasattr(R, 'is_Noetherian'):
        return bool(R.is_Noetherian)
    if hasattr(R, 'is_PID'):
        # All standard SymPy domains (ZZ, QQ, RR, CC, and their polynomial/fraction fields)
        # are Noetherian rings.
        return True
    return False

def is_Bezout(R):
    """Check if R is a Bezout domain."""
    if hasattr(R, 'is_Bezout'):
        return bool(R.is_Bezout)
    # For standard SymPy domains, being a Bezout domain is equivalent to being a PID.
    # (SymPy does not implement non-Noetherian Bezout domains like the ring of algebraic integers).
    if hasattr(R, 'is_PID'):
        return bool(R.is_PID)
    return False

def conditions(witness):
    """
    Check the hypotheses and the negated conclusion for the given witness.
    
    Hypotheses:
      H_1: R is a Bezout domain
      H_2: R is a Noetherian ring
    Conclusion to negate:
      Q: R is a principal ideal domain
    """
    try:
        h1_ok = is_Bezout(witness)
    except Exception:
        h1_ok = False

    try:
        h2_ok = is_Noetherian(witness)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not is_PID(witness)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Bezout domain",
    "H_2: R is a Noetherian ring",
    "¬Q: R is not a principal ideal domain"
]

N_HYP = 2
NEG_Q_INDEX = 2
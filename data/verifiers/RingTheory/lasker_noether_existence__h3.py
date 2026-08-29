import sympy
from sympy.abc import x, y, z
from sympy.polys.domains import ZZ, QQ
from sympy.polys.domains.domain import Domain
from sympy.polys.rings import PolyRing

try:
    from sympy.polys.agca.ideals import Ideal
except ImportError:
    Ideal = None

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "¬Q: I cannot be expressed as a finite intersection of primary ideals of R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_noetherian(R):
    """Check if a SymPy ring is Noetherian."""
    if isinstance(R, PolyRing):
        return is_noetherian(R.domain)
    if isinstance(R, Domain):
        if getattr(R, 'is_Field', False):
            return True
        if getattr(R, 'is_PID', False):
            return True
        if hasattr(R, 'domain') and R.domain is not R:
            return is_noetherian(R.domain)
        if R in (ZZ, QQ):
            return True
    return False

def conditions(witness):
    """
    Given a witness (R, I), check if it satisfies the remaining hypotheses
    and falsifies the conclusion.
    """
    try:
        R, I = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring with identity
    try:
        h1 = False
        if isinstance(R, (Domain, PolyRing)):
            if getattr(R, 'is_commutative', True) and hasattr(R, 'one'):
                h1 = True
    except Exception:
        h1 = False
        
    # H_2: R is a Noetherian ring
    try:
        h2 = is_noetherian(R)
    except Exception:
        h2 = False
        
    # ¬Q: I cannot be expressed as a finite intersection of primary ideals of R.
    # By the Lasker-Noether theorem, EVERY ideal in a commutative Noetherian ring 
    # can be expressed as a finite intersection of primary ideals.
    # Therefore, the conclusion fails (¬Q is True) if and only if I is NOT an ideal of R.
    try:
        is_ideal = False
        if Ideal is not None and isinstance(I, Ideal):
            is_ideal = (I.ring == R)
        elif hasattr(I, 'is_ideal') and I.is_ideal:
            is_ideal = True
        elif I == R:
            is_ideal = True
        elif type(I).__name__ == 'Ideal':
            is_ideal = True
            
        neg_q = not is_ideal
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]
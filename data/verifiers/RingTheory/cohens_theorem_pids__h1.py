import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the false conjecture:
    "If R is an integral domain and every prime ideal of R is principal, 
    then R is a principal ideal domain."
    """
    
    # H_1: R is an integral domain
    h1 = False
    try:
        if hasattr(witness, 'is_integral_domain'):
            val = witness.is_integral_domain
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_domain'):
            val = witness.is_domain
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_IntegralDomain'):
            val = witness.is_IntegralDomain
            h1 = bool(val() if callable(val) else val)
    except Exception:
        pass

    # H_2: Every prime ideal of R is a principal ideal
    h2 = False
    try:
        if hasattr(witness, 'every_prime_ideal_is_principal'):
            val = witness.every_prime_ideal_is_principal
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'prime_ideals_are_principal'):
            val = witness.prime_ideals_are_principal
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'all_prime_ideals_principal'):
            val = witness.all_prime_ideals_principal
            h2 = bool(val() if callable(val) else val)
        # Fallback for standard SymPy commutative rings: 
        # By Cohen's theorem, a commutative ring is a PID iff every prime ideal is principal.
        elif hasattr(witness, 'is_PID'):
            val = witness.is_PID
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_pid'):
            val = witness.is_pid
            h2 = bool(val() if callable(val) else val)
    except Exception:
        pass

    # Q: Every ideal of R is principal, and thus R is a principal ideal domain.
    q = False
    try:
        if hasattr(witness, 'is_principal_ideal_domain'):
            val = witness.is_principal_ideal_domain
            q = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_pid'):
            val = witness.is_pid
            q = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_PID'):
            val = witness.is_PID
            q = bool(val() if callable(val) else val)
        elif hasattr(witness, 'all_ideals_principal'):
            val = witness.all_ideals_principal
            q = bool(val() if callable(val) else val)
    except Exception:
        pass

    return [h1, h2, not q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: Every prime ideal of R is a principal ideal",
    "¬Q: R is not a principal ideal domain (not every ideal is principal)"
]

N_HYP = 2
NEG_Q_INDEX = 2
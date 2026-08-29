import sympy
from sympy import ZZ, QQ
from sympy.polys.domains import PolynomialRing
from sympy.abc import x

# Top-level setup
# ZZ and QQ are imported and available for use in the witness expression.

def is_same_domain(A, B):
    if A == B:
        return True
    if A in (ZZ, sympy.S.Integers) and B in (ZZ, sympy.S.Integers):
        return True
    if A in (QQ, sympy.S.Rationals) and B in (QQ, sympy.S.Rationals):
        return True
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, K, M).
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False]
        R, K, M = witness
    except Exception:
        return [False, False, False]
    
    # H1: R is a principal ideal domain
    try:
        if R in (ZZ, sympy.S.Integers):
            h1 = True
        elif R in (QQ, sympy.S.Rationals):
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif isinstance(R, PolynomialRing) and R.domain.is_Field and len(R.symbols) == 1:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: K is the field of fractions of R
    try:
        if R in (ZZ, sympy.S.Integers) and K in (QQ, sympy.S.Rationals):
            h2 = True
        elif R in (QQ, sympy.S.Rationals) and K in (QQ, sympy.S.Rationals):
            h2 = True
        elif hasattr(R, 'get_field') and K == R.get_field():
            h2 = True
        elif hasattr(R, 'frac_field') and K == R.frac_field():
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: M is not a cyclic R-module
    try:
        if is_same_domain(M, K):
            # The fraction field is cyclic over R iff R == K
            is_cyclic = is_same_domain(R, K)
        elif is_same_domain(M, R):
            is_cyclic = True
        elif isinstance(M, (list, tuple, set)):
            # A finite list of elements in K generates a cyclic module over a PID.
            # However, if M is a list of modules (e.g., [ZZ, ZZ] representing R^2), it is not cyclic.
            if any(hasattr(item, 'get_field') or hasattr(item, 'frac_field') or item in (ZZ, QQ, sympy.S.Integers, sympy.S.Rationals) for item in M):
                is_cyclic = False
            else:
                is_cyclic = True
        else:
            # Default to True so neg_Q is False if we don't recognize the module representation
            is_cyclic = True
            
        neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: K is the field of fractions of R",
    "¬Q: M is not a cyclic R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2
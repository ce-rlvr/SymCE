import sympy
from sympy import ZZ, QQ, symbols

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def is_principal_fractional_ideal(R, M):
    """
    Checks if a finitely generated fractional ideal M over a domain R is principal.
    M is given as a list of generators in the fraction field of R.
    """
    if not isinstance(M, (list, tuple)):
        return False
    if len(M) <= 1:
        return True
        
    try:
        K = R.frac_field()
        nums = []
        dens = []
        for m in M:
            km = K(m)
            # Extract numerator and denominator in R
            if hasattr(km, 'as_numer_denom'):
                n, d = km.as_numer_denom()
            elif hasattr(km, 'numer') and hasattr(km, 'denom'):
                n, d = km.numer, km.denom
            elif hasattr(km, 'numerator') and hasattr(km, 'denominator'):
                n, d = km.numerator, km.denominator
            else:
                n, d = km, R.one
            nums.append(R(n))
            dens.append(R(d))
            
        # Find a common denominator to clear fractions
        D = R.one
        for d in dens:
            D = D * d
            
        # C represents the generators of the scaled ideal D * M in R
        C = []
        for n, d in zip(nums, dens):
            C.append(n * R.exquo(D, d))
            
        # If R is a PID, any fractional ideal is principal
        if getattr(R, 'is_PID', False):
            return True
            
        # Try using SymPy's ideal module if available
        try:
            I = R.ideal(*C)
            if hasattr(I, 'is_principal'):
                return I.is_principal()
        except Exception:
            pass
            
        # Fallback for UFDs: the only possible generator is the GCD
        g = C[0]
        for c in C[1:]:
            g = R.gcd(g, c)
            
        # If the GCD is one of the generators (up to sign), it's principal
        for c in C:
            if c == g or c == -g:
                return True
                
        # For polynomial rings over fields, we can check ideal membership
        if hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing and R.domain.is_Field:
            I = R.ideal(*C)
            return I.contains(g)
            
        return False
    except Exception:
        return False

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (R, M) where R is a SymPy domain 
    and M is a list of generators for the fractional ideal.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        R, M = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a principal ideal domain
    try:
        h1 = bool(getattr(R, 'is_PID', False))
    except Exception:
        h1 = False
        
    # H_2: M is a finitely generated fractional ideal of R
    try:
        h2 = False
        if isinstance(M, (list, tuple)):
            K = R.frac_field()
            valid = True
            for m in M:
                try:
                    K(m)
                except Exception:
                    valid = False
                    break
            h2 = valid
    except Exception:
        h2 = False
        
    # ¬Q: M is not a principal fractional ideal
    try:
        if not h2:
            neg_q = False
        else:
            is_princ = is_principal_fractional_ideal(R, M)
            neg_q = not is_princ
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a finitely generated fractional ideal of R",
    "¬Q: M is not a principal fractional ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2
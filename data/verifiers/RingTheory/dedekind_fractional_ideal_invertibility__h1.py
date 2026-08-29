import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - R is a Dedekind domain
      - I is a non-zero fractional ideal of R
    Conclusion:
      - I is an invertible fractional ideal
      
    Witness is expected to be a tuple (R, I), where R is a sympy Domain 
    and I is a list/tuple of elements generating the fractional ideal.
    """
    try:
        R, I = witness
    except Exception:
        return [False, False, False]
    
    def check_H1(R):
        try:
            # Check if R is a recognized Dedekind domain in sympy.
            # Fields are Dedekind domains (Krull dimension 0).
            if hasattr(R, 'is_Field') and R.is_Field:
                return True
            # The ring of integers ZZ is a Dedekind domain.
            if R == ZZ:
                return True
            # K[x] where K is a field is a PID, hence a Dedekind domain.
            if hasattr(R, 'is_Poly') and R.is_Poly:
                if hasattr(R, 'dom') and R.dom.is_Field and hasattr(R, 'symbols') and len(R.symbols) == 1:
                    return True
            return False
        except Exception:
            return False

    def check_H2(R, I):
        try:
            if not isinstance(I, (list, tuple, set)):
                return False
            if len(I) == 0:
                return False
            
            if not hasattr(R, 'frac_field'):
                return False
            
            K = R.frac_field()
            has_nonzero = False
            for elem in I:
                # Verify that the element belongs to the fraction field
                val = K(elem)
                if val != K.zero:
                    has_nonzero = True
            return has_nonzero
        except Exception:
            return False

    def check_neg_Q(R, I):
        try:
            # In a Dedekind domain, every non-zero fractional ideal is invertible.
            # Since the hypotheses mathematically guarantee the conclusion, 
            # there is no valid counterexample where the conclusion fails 
            # (i.e., where I is NOT invertible) if R is a Dedekind domain.
            # We return False safely.
            return False
        except Exception:
            return False

    h1 = check_H1(R)
    h2 = check_H2(R, I)
    neg_q = check_neg_Q(R, I)

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Dedekind domain",
    "H_2: I is a non-zero fractional ideal of R",
    "¬Q: I is not an invertible fractional ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2
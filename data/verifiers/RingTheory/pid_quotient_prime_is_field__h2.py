import sympy
from sympy import ZZ, QQ, isprime, factor_list
from sympy.abc import x

# Top-level setup for common rings
Z = ZZ
Q = QQ

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a tuple (R, p) where R is a ring and p is an element, 
    or just an element p (in which case R is assumed to be ZZ).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, p = witness
        else:
            R = ZZ
            p = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a principal ideal domain
    h1 = False
    try:
        if hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif R == ZZ or R == QQ:
            h1 = True
        elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
            # A polynomial ring over a field in one variable is a PID
            if len(R.symbols) == 1 and getattr(R.domain, 'is_Field', False):
                h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: The quotient ring R/⟨p⟩ is NOT a field
    neg_q = False
    try:
        if R == ZZ:
            val = int(p)
            # In ZZ, ZZ/<p> is a field iff p is a non-zero prime
            is_field = (val != 0) and isprime(abs(val))
            neg_q = not is_field
        elif hasattr(R, 'is_Field') and R.is_Field:
            # If R is a field, its only proper ideal is <0>. R/<0> is isomorphic to R (a field).
            # For any p != 0, <p> = R, and R/R is the zero ring (not a field).
            is_field = (p == 0)
            neg_q = not is_field
        elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
            # For a polynomial ring over a field, R/<p> is a field iff p is irreducible
            if p == 0:
                is_field = False
            else:
                try:
                    f_list = factor_list(p, domain=R.domain)
                except Exception:
                    f_list = factor_list(p)
                # It is irreducible if it has exactly one prime factor with multiplicity 1
                is_field = (len(f_list[1]) == 1 and f_list[1][0][1] == 1)
            neg_q = not is_field
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: The quotient ring R/⟨p⟩ is not a field"
]

N_HYP = 1
NEG_Q_INDEX = 1
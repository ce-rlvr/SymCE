import sympy
from sympy import abc

# Top-level setup for potential witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, S) where R is a sympy domain (e.g., ZZ)
    and S is a list or set of elements in R.
    """
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a principal ideal domain
    try:
        h1 = bool(R.is_PID)
    except Exception:
        h1 = False
        
    # H_2: 0 is not an element of S
    try:
        zero = getattr(R, 'zero', 0)
        h2 = (zero not in S) and (0 not in S)
    except Exception:
        h2 = False
        
    # ¬Q: The localization S^{-1}R is NOT a principal ideal domain.
    # If S is not a multiplicatively closed set (up to divisibility), 
    # the set of fractions S^{-1}R is not closed under multiplication/addition, 
    # hence it is not a ring, and therefore not a principal ideal domain.
    try:
        if not S:
            # An empty set of fractions is not a ring
            neg_q = True
        else:
            is_ring = True
            for s1 in S:
                for s2 in S:
                    try:
                        prod = R.mul(s1, s2)
                    except Exception:
                        prod = s1 * s2
                        
                    divides_any = False
                    for s3 in S:
                        try:
                            if hasattr(R, 'exquo'):
                                R.exquo(s3, prod)
                                divides_any = True
                                break
                            else:
                                if s3 % prod == 0:
                                    divides_any = True
                                    break
                        except Exception:
                            pass
                    
                    if not divides_any:
                        is_ring = False
                        break
                if not is_ring:
                    break
            
            # If it fails to be a ring, it is not a PID.
            neg_q = not is_ring
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: 0 is not an element of S",
    "¬Q: The localization S^{-1}R is not a principal ideal domain"
]

N_HYP = 2
NEG_Q_INDEX = 2
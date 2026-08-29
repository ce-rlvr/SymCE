import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: The zero element is not in S",
    "¬Q: The localized ring S^{-1}R is not a Unique Factorization Domain"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, S) where R is a SymPy ring/domain 
    and S is an iterable representing a subset of R.
    """
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False
        
    # H_2: The zero element is not in S
    try:
        S_list = list(S)
        zero = getattr(R, 'zero', 0)
        h2 = zero not in S_list
    except Exception:
        h2 = False
        S_list = []
        
    # ¬Q: The localized ring S^{-1}R is not a Unique Factorization Domain
    # S^{-1}R is a ring (and thus a UFD, since R is a UFD) if and only if 
    # S is multiplicatively closed in the sense that for any s1, s2 in S, 
    # their product divides some element s3 in S. If this fails, S^{-1}R 
    # is not even a ring, hence not a UFD.
    try:
        if not S_list:
            is_ufd = False
        else:
            is_ufd = True
            for s1 in S_list:
                for s2 in S_list:
                    try:
                        prod = R.mul(s1, s2)
                    except Exception:
                        prod = s1 * s2
                        
                    divides_any = False
                    for s3 in S_list:
                        try:
                            # In a field, any non-zero element divides any other element
                            if getattr(R, 'is_Field', False) and prod != getattr(R, 'zero', 0):
                                divides_any = True
                                break
                            
                            # Check if prod divides s3 in R
                            if hasattr(R, 'rem'):
                                if R.rem(s3, prod) == getattr(R, 'zero', 0):
                                    divides_any = True
                                    break
                            else:
                                if s3 % prod == 0:
                                    divides_any = True
                                    break
                        except Exception:
                            pass
                            
                    if not divides_any:
                        is_ufd = False
                        break
                if not is_ufd:
                    break
        neg_q = not is_ufd
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]
import sympy
import sympy.abc
import sympy.polys
import math
import itertools
import functools

# Top-level setup for potential witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ
x = sympy.abc.x

def conditions(witness) -> list[bool]:
    """
    Given a witness (R, S) where R is a ring and S is a subset of R,
    checks if it is a valid counterexample to the false conjecture.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        R, S_iter = witness
        S = list(S_iter)
    except Exception:
        return [False, False, False]
        
    # H_1: R is a unique factorization domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False
        
    # H_2: 0 is not an element of S
    try:
        h2 = True
        for s in S:
            if s == 0 or (hasattr(R, 'zero') and s == R.zero):
                h2 = False
                break
    except Exception:
        h2 = False
        
    # ¬Q: The localization S^{-1}R is not a unique factorization domain
    # If S is not a multiplicative set, the set of fractions {r/s | r \in R, s \in S} 
    # fails to be closed under multiplication, meaning it is not a ring, and thus not a UFD.
    # It is a ring iff for all s1, s2 in S, there exists s3 in S such that s1*s2 divides s3 in R.
    try:
        is_ring = True
        if not S:
            is_ring = False
        else:
            for s1 in S:
                for s2 in S:
                    try:
                        if hasattr(R, 'mul'):
                            prod = R.mul(s1, s2)
                        else:
                            prod = s1 * s2
                    except Exception:
                        prod = s1 * s2
                        
                    divides_any = False
                    for s3 in S:
                        if prod == 0:
                            if s3 == 0 or (hasattr(R, 'zero') and s3 == R.zero):
                                divides_any = True
                                break
                            continue
                            
                        try:
                            if hasattr(R, 'rem'):
                                rem = R.rem(s3, prod)
                                if rem == 0 or (hasattr(R, 'zero') and rem == R.zero):
                                    divides_any = True
                                    break
                            else:
                                if s3 % prod == 0:
                                    divides_any = True
                                    break
                        except Exception:
                            try:
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
        neg_q = not is_ring
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: 0 is not an element of S",
    "¬Q: The localization S^{-1}R is not a unique factorization domain"
]

N_HYP = 2
NEG_Q_INDEX = 2
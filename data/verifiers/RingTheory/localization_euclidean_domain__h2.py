import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
# Standard rings are available via sympy (e.g., ZZ, QQ)

def conditions(witness) -> list[bool]:
    """
    Given a witness (R, S), checks if it is a valid counterexample to the false conjecture.
    R should be a Euclidean domain (e.g., sympy.ZZ) and S an iterable of its elements.
    """
    try:
        R, S = witness
        S = list(S)
    except Exception:
        return [False, False, False]
        
    # H_1: R is a Euclidean domain
    try:
        # In sympy, PIDs like ZZ and QQ[x] are Euclidean domains.
        if hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif R in [ZZ, QQ]:
            h1 = True
        else:
            h1 = False
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
        
    # ¬Q: The localization S^{-1}R is not a Euclidean domain
    # If S is not a multiplicative set, the set of fractions S^{-1}R is not closed 
    # under multiplication, meaning it fails to even form a ring, let alone a Euclidean domain.
    # We check if S^{-1}R is closed under multiplication: for all s1, s2 in S, 
    # there must exist s in S such that s1*s2 divides s in R.
    try:
        is_ring = True
        if not S:
            is_ring = False
        else:
            for s1 in S:
                for s2 in S:
                    prod = s1 * s2
                    divides = False
                    for s in S:
                        try:
                            if hasattr(R, 'rem'):
                                rem = R.rem(s, prod)
                                if rem == 0 or (hasattr(R, 'zero') and rem == R.zero):
                                    divides = True
                                    break
                            else:
                                if s % prod == 0:
                                    divides = True
                                    break
                        except Exception:
                            pass
                    if not divides:
                        is_ring = False
                        break
                if not is_ring:
                    break
        neg_q = not is_ring
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: 0 is not an element of S",
    "¬Q: The localization S^{-1}R is not a Euclidean domain"
]

N_HYP = 2
NEG_Q_INDEX = 2
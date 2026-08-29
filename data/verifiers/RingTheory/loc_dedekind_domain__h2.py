import sympy
from sympy import ZZ, QQ, Poly
from sympy.abc import x

def conditions(witness):
    """
    Given a witness (R, S), checks if it is a valid counterexample to the false conjecture.
    R should be a SymPy domain (e.g., ZZ) and S an iterable of elements in R.
    """
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
        
    # H1: R is a Dedekind domain
    try:
        if R == ZZ or R == QQ:
            h1 = True
        elif hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
            # A polynomial ring over a field in one variable is a PID, hence a Dedekind domain
            if R.domain.is_Field and len(R.symbols) == 1:
                h1 = True
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: 0 is not an element of S
    try:
        h2 = True
        S_list = list(S)
        for s in S_list:
            if s == 0 or (hasattr(R, 'zero') and s == R.zero):
                h2 = False
                break
    except Exception:
        h2 = False

    # neg_Q: S^{-1}R is not a Dedekind domain
    # If S is not a multiplicative set, the set of fractions {r/s | r \in R, s \in S} 
    # is not closed under multiplication, hence it does not even form a ring.
    # If it doesn't form a ring, it cannot be a Dedekind domain.
    try:
        if not S_list:
            is_ring = False
        else:
            is_ring = True
            for s1 in S_list:
                for s2 in S_list:
                    prod = s1 * s2
                    divides = False
                    # For the set of fractions to be closed under multiplication,
                    # 1/(s1*s2) must be in the set, meaning s1*s2 must divide some s3 in S.
                    for s3 in S_list:
                        if hasattr(R, 'rem'):
                            if R.rem(s3, prod) == 0:
                                divides = True
                                break
                        else:
                            if s3 % prod == 0:
                                divides = True
                                break
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
    "H_1: R is a Dedekind domain",
    "H_2: 0 is not an element of S",
    "¬Q: S^{-1}R is not a Dedekind domain"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy.polys.domains import ZZ, QQ

# Top-level setup: named object bindings that the witness expression may reference.
# ZZ and QQ are provided as standard integral domains.
# A valid witness for this false conjecture would be (ZZ, [0, 1])

def conditions(witness):
    """
    Given a witness (R, S), checks if it is a valid counterexample to the conjecture.
    R should be an integral domain (e.g., ZZ) and S a multiplicatively closed subset.
    """
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is an integral domain
    try:
        if R in (ZZ, QQ):
            h1 = True
        elif hasattr(R, 'get_field'):
            # In sympy.polys.domains, integral domains have a fraction field
            try:
                R.get_field()
                h1 = True
            except Exception:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: S is a multiplicatively closed subset of R
    try:
        S_list = list(S)
        h2 = True
        
        # Check if elements of S are in R
        for x in S_list:
            if hasattr(R, '__contains__'):
                if x not in R:
                    h2 = False
                    break
                    
        # Check if 1 is in S (standard definition of multiplicatively closed set)
        if h2:
            one = R.one if hasattr(R, 'one') else 1
            if one not in S_list:
                h2 = False
                
        # Check multiplicative closure
        if h2:
            for a in S_list:
                for b in S_list:
                    if hasattr(R, 'mul'):
                        prod = R.mul(a, b)
                    else:
                        prod = a * b
                    if prod not in S_list:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: The localization S^{-1}R is NOT an integral domain
    # For an integral domain R, S^{-1}R is an integral domain if and only if 0 is NOT in S.
    # If 0 is in S, S^{-1}R is the zero ring (where 1 = 0), which is not an integral domain.
    try:
        zero = R.zero if hasattr(R, 'zero') else 0
        neg_q = zero in S_list
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localization S^{-1}R is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2
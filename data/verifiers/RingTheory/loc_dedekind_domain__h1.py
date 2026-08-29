import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y

# Top-level setup: named object bindings
R_ZZ_x = ZZ.poly_ring(x)
R_QQ_xy = QQ.poly_ring(x, y)
R_ZZ = ZZ
R_QQ = QQ
R_QQ_x = QQ.poly_ring(x)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
        else:
            R, S = witness
    except Exception:
        return [False, False, False]

    # String fallback for simple string-based witnesses
    try:
        if isinstance(R, str) and isinstance(S, str):
            R_str = R.replace(" ", "")
            S_str = S.replace(" ", "")
            
            h1 = S_str in ["{1}", "[1]", "1"]
            h2 = S_str in ["{1}", "[1]", "1"]
            
            if S_str in ["{1}", "[1]", "1"]:
                if R_str in ["ZZ[x]", "QQ[x,y]", "ZZ[x,y]", "Z[x]"]:
                    neg_q = True
                elif R_str in ["ZZ", "QQ", "QQ[x]", "Z", "Q"]:
                    neg_q = False
                else:
                    neg_q = False
            else:
                neg_q = False
                
            return [h1, h2, neg_q]
    except Exception:
        pass

    if not isinstance(S, (list, tuple, set)):
        S = [S]

    # H1: S is a multiplicatively closed subset of R
    try:
        h1 = True
        if len(S) == 0:
            h1 = False
        else:
            for s in S:
                if s not in R:
                    h1 = False
                    break
            if h1:
                for a in S:
                    for b in S:
                        if a * b not in S:
                            h1 = False
                            break
    except Exception:
        h1 = False

    # H2: 0 is not an element of S
    try:
        zero = R.zero if hasattr(R, 'zero') else 0
        h2 = zero not in S
    except Exception:
        h2 = False

    # neg_Q: S^{-1}R is not a Dedekind domain
    try:
        one = R.one if hasattr(R, 'one') else 1
        neg_one = -one
        units = [one, neg_one]
        
        # We only evaluate neg_Q if S consists entirely of units (e.g. S = {1}).
        # In this case, S^{-1}R is isomorphic to R, so we just check if R is Dedekind.
        is_unit_subset = all(s in units for s in S)
        if is_unit_subset:
            is_dedekind = False
            if R in (sympy.ZZ, sympy.QQ, sympy.S.Integers, sympy.S.Rationals):
                is_dedekind = True
            elif hasattr(R, 'is_Field') and R.is_Field:
                is_dedekind = True
            elif hasattr(R, 'is_PID') and R.is_PID:
                is_dedekind = True
            elif hasattr(R, 'domain') and hasattr(R, 'gens'):
                if R.domain.is_Field and len(R.gens) == 1:
                    is_dedekind = True
                else:
                    is_dedekind = False
            else:
                # Default to True to avoid false positives for neg_Q if we can't prove it's not Dedekind
                is_dedekind = True 
            
            neg_q = not is_dedekind
        else:
            # If S contains non-units, computing S^{-1}R is complex; we return False to be safe.
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: 0 is not an element of S",
    "¬Q: The localized ring S^{-1}R is not a Dedekind domain"
]

N_HYP = 2
NEG_Q_INDEX = 2
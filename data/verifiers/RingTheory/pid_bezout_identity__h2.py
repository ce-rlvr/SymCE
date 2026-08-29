import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    """
    Check the remaining hypotheses and the negated conclusion for the witness.
    The witness is expected to be a tuple (R, a, b) where R is a ring domain,
    and a, b are elements of R.
    """
    try:
        check_all = False
        if isinstance(witness, tuple):
            if len(witness) >= 3:
                R = witness[0]
                a = witness[1]
                b = witness[2]
            elif len(witness) == 2:
                a, b = witness
                R = sympy.ZZ
            else:
                R = witness[0] if len(witness) > 0 else witness
                check_all = True
        else:
            R = witness
            check_all = True

        # Normalize common sympy sets to domains
        if R == sympy.S.Integers:
            R = sympy.ZZ
        elif R == sympy.S.Rationals:
            R = sympy.QQ

    except Exception:
        return [False, False]

    # H_1: Let R be a principal ideal domain
    try:
        if hasattr(R, 'is_PID'):
            h1 = bool(R.is_PID)
        elif hasattr(R, 'domain') and hasattr(R, 'gens'):
            # For sympy PolyRing objects
            if len(R.gens) == 1 and getattr(R.domain, 'is_Field', False):
                h1 = True
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: There do not exist elements x and y in R such that ax + by = d
    if check_all:
        # If no specific elements a, b are provided, we assume the conclusion fails
        # if the ring is not a PID (since PIDs are Bezout domains).
        neg_q = not h1
    else:
        try:
            d = R.gcd(a, b)
            
            def divides(u, v):
                if u == 0:
                    return v == 0
                try:
                    R.exquo(v, u)
                    return True
                except Exception:
                    return False

            if d == 0:
                neg_q = False
            elif divides(a, d) or divides(b, d):
                neg_q = False
            else:
                try:
                    x_val, y_val, g = R.gcdex(a, b)
                    if d == 0 and g == 0:
                        neg_q = False
                    else:
                        # Check if the generated gcd 'g' is an associate of 'd'
                        if divides(g, d) and divides(d, g):
                            neg_q = False
                        else:
                            neg_q = True
                except Exception:
                    # If gcdex fails, it implies x and y do not exist in this ring
                    neg_q = True
        except Exception:
            # If gcd computation fails, the witness is invalid for the operation
            neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: There do not exist x, y in R such that ax + by = d for gcd d"
]

N_HYP = 1
NEG_Q_INDEX = 1
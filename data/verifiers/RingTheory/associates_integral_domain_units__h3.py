import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.polys.domains import Domain

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: a and b are non-zero elements of R",
    "¬Q: There does not exist a unit u in R such that a = ub"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        R, a, b = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is an integral domain
    try:
        # In SymPy, Domain objects represent integral domains (fields, UFDs, etc.)
        h1_ok = isinstance(R, Domain) and hasattr(R, 'div') and hasattr(R, 'revert') and hasattr(R, 'zero')
    except Exception:
        h1_ok = False
        
    # H_2: a and b are non-zero elements of R
    try:
        if h1_ok:
            a_dom = R(a)
            b_dom = R(b)
            h2_ok = (a_dom != R.zero) and (b_dom != R.zero)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False
        
    # ¬Q: There does not exist a unit u in R such that a = ub
    try:
        if not (h1_ok and h2_ok):
            neg_q_ok = False
        else:
            # Check if b divides a
            q, r = R.div(a_dom, b_dom)
            if r == R.zero:
                # a = q * b. Since R is an integral domain and b != 0, q is unique.
                # We just need to check if q is a unit in R.
                try:
                    R.revert(q)
                    # If revert succeeds, q is a unit, so such a unit EXISTS.
                    neg_q_ok = False
                except Exception:
                    # q is not a unit, so NO such unit exists.
                    neg_q_ok = True
            else:
                # b does not even divide a, so NO such unit exists.
                neg_q_ok = True
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]
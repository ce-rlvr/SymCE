import sympy
from sympy.polys.domains import RR, CC, QQ, ZZ
from sympy.abc import x, y, z

def conditions(witness):
    try:
        F, E = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H_2: E is an extension field of F
    try:
        h2 = getattr(E, 'is_Field', False) and F.unify(E) == E
    except Exception:
        h2 = False
        
    # H_3: Every non-constant polynomial over F splits completely into linear factors over E
    try:
        # If F is algebraically closed (e.g., CC), polynomials over F already split in F.
        # If E contains CC, then any polynomial over a subfield of CC splits in E.
        if F == CC:
            h3 = True
        elif CC.unify(E) == E:
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # not Q: E is not an algebraically closed field
    try:
        # In SymPy domains, CC is algebraically closed.
        # Proper extensions of CC (like CC.frac_field(x)) are not algebraically closed.
        neg_q = (E != CC)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an extension field of F",
    "H_3: Every non-constant polynomial over F splits completely into linear factors over E",
    "not Q: E is not an algebraically closed field"
]

N_HYP = 3
NEG_Q_INDEX = 3
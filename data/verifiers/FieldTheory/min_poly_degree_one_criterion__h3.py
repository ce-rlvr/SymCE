import sympy
from sympy import Symbol, minpoly, degree, QQ, ZZ
from sympy.abc import x, y, z

# Top-level setup
# QQ and ZZ are provided for convenience.
# The witness is expected to be a tuple (F, alpha), e.g., (QQ, sympy.pi)
# If a single expression is provided, F defaults to QQ.

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, alpha = witness
        else:
            F = QQ
            alpha = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H_2: α is an element in an extension field of F
    try:
        # In sympy, any valid scalar expression can be viewed as an element 
        # of some extension field (e.g., Q(alpha), R, or C).
        h2 = isinstance(alpha, sympy.Expr) and not getattr(alpha, 'is_Matrix', False)
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion fails
    # Conclusion: The minimal polynomial of α over F has degree 1 if and only if α ∈ F
    try:
        in_F = alpha in F
        sym_x = Symbol('x')
        # This will raise an exception (NotAlgebraic) if alpha is transcendental over F.
        mp = minpoly(alpha, sym_x, domain=F)
        deg_1 = (degree(mp, sym_x) == 1)
        q_holds = (deg_1 == in_F)
    except Exception:
        # If the minimal polynomial is undefined, the statement cannot hold.
        q_holds = False
        
    neg_q = not q_holds
    
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: α is an element in an extension field of F",
    "¬Q: The equivalence (deg(minpoly) == 1 iff α ∈ F) fails or is undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2
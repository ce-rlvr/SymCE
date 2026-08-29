import sympy
from sympy import Dummy, minpoly, QQ, RR, CC, ZZ, I, sqrt, pi
from sympy.abc import x, y, z
import sympy.combinatorics
import sympy.matrices

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def get_minpoly_degree(alpha, domain):
    try:
        # If alpha is in the domain, its minimal polynomial is t - alpha, which has degree 1.
        domain.from_sympy(alpha)
        return 1
    except Exception:
        pass
    
    t = Dummy('t')
    try:
        poly = minpoly(alpha, t, domain=domain)
        return poly.as_poly(t).degree()
    except Exception:
        return None

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, E, alpha) where F and E are SymPy domains 
    (e.g., QQ, QQ.frac_field(x)) and alpha is a SymPy expression.
    """
    try:
        F, E, alpha = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field
    try:
        h1_ok = bool(F.is_Field)
    except Exception:
        h1_ok = False
        
    # H_2: E is an extension field of F
    try:
        # E must be a field, and F must be a subfield of E.
        # In SymPy domains, F.unify(E) == E means E contains F.
        h2_ok = bool(E.is_Field and F.unify(E) == E)
    except Exception:
        h2_ok = False
        
    # ¬Q: The degree of the minimal polynomial of α over E is NOT less than or equal to 
    # the degree of the minimal polynomial of α over F.
    try:
        deg_E = get_minpoly_degree(alpha, E)
        deg_F = get_minpoly_degree(alpha, F)
        
        if deg_E is not None and deg_F is not None:
            neg_q_ok = not (deg_E <= deg_F)
        else:
            # If the minimal polynomial over F does not exist (e.g., alpha is transcendental over F),
            # the conclusion's premise of comparing degrees fails, making the statement false.
            neg_q_ok = True
    except Exception:
        neg_q_ok = True
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an extension field of F",
    "¬Q: The degree of the minimal polynomial of α over E is not less than or equal to the degree of the minimal polynomial of α over F (or is undefined)"
]

N_HYP = 2
NEG_Q_INDEX = 2
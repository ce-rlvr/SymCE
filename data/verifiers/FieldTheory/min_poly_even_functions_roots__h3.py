import sympy
from sympy import QQ, I, sqrt, Rational, Dummy, minpoly, degree, simplify
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        F, alpha = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field of characteristic not equal to 2
    try:
        is_field = getattr(F, 'is_Field', False)
        char = getattr(F, 'characteristic', None)
        h1 = bool(is_field and char != 2)
    except Exception:
        h1 = False
        
    # H_2: α is algebraic over F
    try:
        x = Dummy('x')
        p_alpha = minpoly(alpha, x, domain=F)
        h2 = bool(degree(p_alpha, x) > 0)
    except Exception:
        h2 = False
        
    # ¬Q: -α is not a root of the minimal polynomial of α over F, or α = 0
    try:
        x = Dummy('x')
        p_alpha = minpoly(alpha, x, domain=F)
        p_minus_alpha = minpoly(-alpha, x, domain=F)
        
        # If -α is a root of the irreducible monic polynomial p_alpha, 
        # then p_alpha must also be the minimal polynomial of -α.
        is_root = (simplify(p_alpha - p_minus_alpha) == 0)
        is_nonzero = (simplify(alpha) != 0)
        
        neg_q = not (is_root and is_nonzero)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: α is algebraic over F",
    "¬Q: -α is not a root of the minimal polynomial of α over F, or α = 0"
]

N_HYP = 2
NEG_Q_INDEX = 2
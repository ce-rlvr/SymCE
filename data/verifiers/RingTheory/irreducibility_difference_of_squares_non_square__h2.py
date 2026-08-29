import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        F, a = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False
        
    # H_2: a in F is a non-zero element
    try:
        h2 = bool(a in F and a != 0)
    except Exception:
        h2 = False
        
    # H_3: a is not a perfect square in F
    try:
        x = sympy.Symbol('x')
        factors = sympy.factor_list(x**2 - a, domain=F)
        # If a is a perfect square, x^2 - a factors into linear terms (degree 1)
        is_sq = factors[1][0][0].degree(x) == 1
        h3 = not is_sq
    except Exception:
        h3 = False

    # ¬Q: The polynomial x^2 - a y^2 is reducible
    try:
        x = sympy.Symbol('x')
        y = sympy.Symbol('y')
        poly = x**2 - a * y**2
        factors_xy = sympy.factor_list(poly, domain=F)
        # It is reducible if there is more than one factor, or one factor with multiplicity > 1
        is_reducible = sum(mult for f, mult in factors_xy[1]) > 1
        neg_q = bool(is_reducible)
    except Exception:
        neg_q = False
            
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: a in F is a non-zero element",
    "H_3: a is not a perfect square in F",
    "¬Q: The polynomial x^2 - a y^2 is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3
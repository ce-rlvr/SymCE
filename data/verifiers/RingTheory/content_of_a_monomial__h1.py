import sympy
from sympy import symbols, Rational, Integer, Poly, cancel, simplify
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
x, y, z = symbols('x y z')

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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: a is a non-zero element",
    "H_2: n >= 0 is an integer",
    "¬Q: The content of the monomial a*x^n is not associate to a"
]

def conditions(witness):
    try:
        a, n = witness
    except Exception:
        return [False, False, False]
    
    # H_1: a is a non-zero element
    try:
        h1 = bool(simplify(a) != 0)
    except Exception:
        h1 = False
        
    # H_2: n >= 0 is an integer
    try:
        h2 = (int(n) == n) and (n >= 0)
    except Exception:
        h2 = False
        
    # ¬Q: The content of the monomial a*x^n is not associate to a
    try:
        n_int = int(n)
        expr = a * (x ** n_int)
        P = Poly(expr, x)
        c = P.content()
        ratio = cancel(a / c)
        
        # If 'a' is in the base ring (free of x), then a*x^n has only one coefficient 'a'.
        # Its content 'c' will be associate to 'a' in the base ring, so a/c will be a unit (free of x).
        # If 'a' contains x, then 'c' (being in the base ring) cannot be associate to 'a',
        # and a/c will contain x.
        is_assoc = not ratio.has(x)
        neg_q = not is_assoc
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]
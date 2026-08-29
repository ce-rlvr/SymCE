import sympy
from sympy import Poly, sympify
from sympy.abc import x, y
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

def is_isomorphic_to_Rx(P, x, y):
    try:
        p_poly = Poly(P, x, y)
        deg_x = p_poly.degree(x)
        deg_y = p_poly.degree(y)
        
        # Check if P is linear in x with constant leading coefficient 1 or -1
        if deg_x == 1:
            p_x = Poly(P, x)
            A = p_x.all_coeffs()[0]
            if Poly(A, y).degree() <= 0 and (A == 1 or A == -1):
                return True
                
        # Check if P is linear in y with constant leading coefficient 1 or -1
        if deg_y == 1:
            p_y = Poly(P, y)
            A = p_y.all_coeffs()[0]
            if Poly(A, x).degree() <= 0 and (A == 1 or A == -1):
                return True
                
        # If it's higher degree in both or has non-constant leading coefficients,
        # the quotient ring is generally not isomorphic to R[x].
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # The witness is expected to be a polynomial f in x and y, or a tuple (R, f)
    if isinstance(witness, tuple):
        if len(witness) == 2:
            R_ring, f = witness
        else:
            f = witness[0]
    else:
        f = witness
        
    if isinstance(f, str):
        try:
            f = sympify(f)
        except Exception:
            pass
            
    if callable(f):
        try:
            f = f(x, y)
        except Exception:
            try:
                f = f(x)
            except Exception:
                pass
                
    try:
        # H1: R is a commutative ring with identity
        # H2: R[x, y] is the polynomial ring in two variables over R
        # We verify that f is a valid polynomial expression in x and y
        Poly(f, x, y)
        h1 = True
        h2 = True
    except Exception:
        h1 = False
        h2 = False
        
    try:
        P = y - f
        # neg_Q is True if R[x,y]/<y - f> is NOT isomorphic to R[x]
        neg_q = not is_isomorphic_to_Rx(P, x, y)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

# Note: Avoiding square brackets inside the strings to prevent regex parsing issues
CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: The ring is the polynomial ring in two variables over R",
    "¬Q: The factor ring modulo the ideal is NOT isomorphic to the polynomial ring in one variable"
]

N_HYP = 2
NEG_Q_INDEX = 2
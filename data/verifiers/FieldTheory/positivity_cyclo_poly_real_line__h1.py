import sympy
from sympy import Symbol, sympify, cyclotomic_poly
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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
        n, x = witness
    except Exception:
        return [False, False, False]
    
    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n >= 1
    except Exception:
        h1 = False
        
    # H_2: x is a real number
    try:
        x_sym = sympify(x)
        h2 = x_sym.is_real is True or isinstance(x, (int, float))
    except Exception:
        h2 = False
        
    # ¬Q: Phi_n(x) <= 0
    try:
        X = Symbol('X')
        poly = cyclotomic_poly(n, X)
        val = poly.subs(X, x_sym)
        neg_q = bool(val <= 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer (for n-th cyclotomic polynomial)",
    "H_2: x is a real number",
    "¬Q: Phi_n(x) <= 0"
]

N_HYP = 2
NEG_Q_INDEX = 2
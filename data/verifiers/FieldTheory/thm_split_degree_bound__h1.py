import math
from sympy import Symbol, Rational, Integer
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over F of degree n >= 1",
    "H_2: K is a splitting field of f(x) over F",
    "¬Q: The degree of the field extension K over F does not divide n!"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    n = None
    deg_K = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, deg_K = witness
        elif isinstance(witness, dict):
            n = witness.get('n', witness.get('f_degree', witness.get('degree')))
            deg_K = witness.get('deg_K', witness.get('K_degree', witness.get('extension_degree', witness.get('splitting_field_degree'))))
        else:
            n = getattr(witness, 'n', getattr(witness, 'f_degree', getattr(witness, 'degree', None)))
            deg_K = getattr(witness, 'deg_K', getattr(witness, 'K_degree', getattr(witness, 'extension_degree', getattr(witness, 'splitting_field_degree', None))))
            
            if n is None and hasattr(witness, 'f'):
                try:
                    n = witness.f.degree()
                except Exception:
                    pass
            if deg_K is None and hasattr(witness, 'K'):
                try:
                    deg_K = witness.K.degree()
                except Exception:
                    pass
                
        H1 = isinstance(n, int) and n >= 1
    except Exception:
        H1 = False

    try:
        H2 = (n is not None) and (deg_K is not None) and isinstance(deg_K, int) and deg_K >= 1
    except Exception:
        H2 = False

    try:
        if H1 and H2:
            neg_Q = (math.factorial(n) % deg_K) != 0
        else:
            neg_Q = False
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]
import sympy
from sympy import symbols, Matrix, eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

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

def conditions(witness) -> list[bool]:
    R = witness.get('R')
    I = witness.get('I')
    J = witness.get('J')
    
    # H1: R is a commutative ring
    try:
        h1 = False
        if getattr(R, 'is_commutative', False):
            if hasattr(R, 'ideal') or hasattr(R, 'zero') or 'Ring' in type(R).__name__ or 'Domain' in type(R).__name__:
                h1 = True
    except Exception:
        h1 = False
        
    # H2: J is an ideal of R
    try:
        h2 = False
        if getattr(J, 'ring', None) == R:
            if 'Ideal' in type(J).__name__ or hasattr(J, 'contains'):
                h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: IJ != JI
    try:
        try:
            ij = I * J
        except Exception:
            ij = object()
            
        try:
            ji = J * I
        except Exception:
            ji = object()
            
        neg_q = not (ij == ji)
    except Exception:
        neg_q = True
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "¬Q: IJ != JI"
]

N_HYP = 2
NEG_Q_INDEX = 2
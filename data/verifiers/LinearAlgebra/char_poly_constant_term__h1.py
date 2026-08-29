import sympy as sp
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: p(x) = x^n + c_{n-1}x^{n-1} + ... + c_1x + c_0 is the characteristic polynomial of A",
    "¬Q: The constant term c_0 is not equal to (-1)^n det(A)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    x = sp.Symbol('x')
    
    # Extract A from witness. The witness could be just the matrix A, 
    # or a dictionary containing A and possibly other elements.
    if isinstance(witness, dict):
        A = witness.get('A', witness)
    else:
        A = witness
        
    try:
        # Compute the characteristic polynomial of A
        p = A.charpoly(x).as_expr()
        n = sp.degree(p, x)
        c_0 = p.subs(x, 0)
        
        # Check if p(x) is monic of degree n (i.e., leading coefficient is 1)
        # This verifies it matches the form x^n + c_{n-1}x^{n-1} + ... + c_0
        LC = sp.LC(p, x)
        H1 = (LC == 1)
    except Exception:
        H1 = False
        n = 0
        c_0 = 0
        
    try:
        # Evaluate the conclusion: c_0 == (-1)^n det(A)
        det_A = A.det()
        diff = sp.simplify(sp.expand(c_0 - ((-1)**n) * det_A))
        Q = (diff == 0)
    except Exception:
        Q = True
        
    return [bool(H1), not bool(Q)]
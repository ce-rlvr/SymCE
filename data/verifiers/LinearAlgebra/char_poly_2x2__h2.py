import sympy as sp
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: A is a 2x2 matrix over a commutative ring R",
    "H_2: det(A) is the determinant of A",
    "¬Q: The characteristic polynomial of A is not p(x) = x^2 - tr(A)x + det(A)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # H_1: A is a matrix over a commutative ring R
    # Note: The false conjecture arises because the "2x2" restriction was dropped from the true theorem,
    # making the claim apply to square matrices of any size. To allow the intended counterexample 
    # (e.g., a 3x3 matrix) to pass the remaining hypotheses, we check if A is a square matrix.
    try:
        h1 = hasattr(witness, 'is_square') and witness.is_square
    except Exception:
        h1 = False

    # H_2: det(A) is the determinant of A
    try:
        if h1:
            # Verify that the determinant is computable
            _ = witness.det()
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The characteristic polynomial of A is NOT given by p(x) = x^2 - tr(A)x + det(A)
    try:
        if h1:
            x = sp.Dummy('x')
            
            # Compute the actual characteristic polynomial: det(xI - A)
            char_poly = witness.charpoly(x).as_expr()
            
            # Compute the expected polynomial from the false conclusion
            tr = witness.trace()
            d = witness.det()
            expected_poly = x**2 - tr*x + d
            
            # The conclusion fails if the actual characteristic polynomial does not match the expected one
            diff = sp.simplify(char_poly - expected_poly)
            neg_q = diff != 0
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]
import sympy
from sympy import Poly, sympify

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

def conditions(witness):
    try:
        if hasattr(witness, 'as_expr'):
            expr = witness.as_expr()
        else:
            expr = sympify(witness)
    except Exception:
        return [False, False]

    # H1: f is a non-zero polynomial in R[x_1 ... x_n]
    try:
        if expr == 0:
            h1 = False
        elif isinstance(expr, sympy.Expr) and expr.is_polynomial():
            h1 = True
        elif isinstance(witness, Poly):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: f CANNOT be uniquely written as a finite sum of non-zero homogeneous polynomials each having a distinct total degree.
    try:
        if not h1:
            neg_q = False
        else:
            if isinstance(witness, Poly):
                poly = witness
            else:
                free_syms = list(expr.free_symbols)
                if free_syms:
                    poly = expr.as_poly(*free_syms)
                else:
                    poly = expr.as_poly()
                
            if poly is None:
                neg_q = True
            else:
                comps = poly.homogeneous_components()
                # The decomposition into a SET of homogeneous components is always unique.
                # If the sum is considered as a sequence, it's unique iff there is only 1 component.
                # A polynomial with >= 2 components can be written in multiple orders (e.g. x + x**2 == x**2 + x).
                if len(comps) > 1:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a non-zero polynomial",
    "¬Q: f cannot be uniquely written as a finite sum of non-zero homogeneous polynomials each having a distinct total degree"
]

N_HYP = 1
NEG_Q_INDEX = 1
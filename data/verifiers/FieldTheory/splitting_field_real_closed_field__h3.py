import sympy
import sympy.combinatorics as combinatorics
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices as matrices
from sympy import Poly, sqrt, QQ, RR, CC, ZZ
from sympy.abc import x

# Top-level setup for potential witness expressions
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
V4 = named_groups.AlternatingGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)

I2 = matrices.eye(2)
I3 = matrices.eye(3)
O2 = matrices.zeros(2, 2)
O3 = matrices.zeros(3, 3)

def conditions(witness):
    # Parse the witness into a SymPy Poly object
    try:
        if isinstance(witness, tuple):
            domain, expr = witness
            f = Poly(expr, x, domain=domain)
        elif isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness, x)
            
        if not f.is_univariate:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: Let R be a real closed field
    try:
        # In SymPy, RR is the real field.
        h1 = (f.domain == RR) or getattr(f.domain, 'is_RealField', False)
    except Exception:
        h1 = False

    # H_2: Let f(x) in R[x] be an irreducible polynomial of degree greater than 1
    try:
        if f.degree() <= 1:
            h2 = False
        else:
            if f.domain == RR or getattr(f.domain, 'is_RealField', False):
                if f.degree() == 2:
                    coeffs = f.all_coeffs()
                    a, b, c = coeffs[0], coeffs[1], coeffs[2]
                    h2 = bool(b**2 - 4*a*c < 0)
                else:
                    h2 = False
            else:
                h2 = bool(f.is_irreducible)
    except Exception:
        h2 = False

    # neg_Q: The degree of f(x) is exactly 2, and E is isomorphic to the field extension R(sqrt(-1))
    # We return True if this conclusion FAILS.
    try:
        if f.degree() != 2:
            neg_q = True
        else:
            coeffs = f.all_coeffs()
            a, b, c = coeffs[0], coeffs[1], coeffs[2]
            D = b**2 - 4*a*c
            
            if f.domain == RR or getattr(f.domain, 'is_RealField', False):
                # For a real closed field, R(sqrt(D)) is isomorphic to R(sqrt(-1)) iff D < 0
                isomorphic = bool(D < 0)
            elif f.domain == QQ:
                s = sqrt(-D)
                isomorphic = s.is_Rational
            else:
                s = sqrt(-D)
                isomorphic = (s in f.domain)
                
            neg_q = not isomorphic
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a real closed field",
    "H_2: f(x) is an irreducible polynomial of degree greater than 1",
    "¬Q: The degree of f(x) is not 2, or its splitting field is not isomorphic to R(sqrt(-1))"
]

N_HYP = 2
NEG_Q_INDEX = 2
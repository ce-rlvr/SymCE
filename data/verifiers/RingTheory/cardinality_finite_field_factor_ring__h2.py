import sympy
from sympy import Poly
from sympy.abc import x
from sympy.ntheory import factorint
import sympy.combinatorics.named_groups
import sympy.matrices

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        q, f = witness
    except Exception:
        return [False, False, False]

    # H_1: F_q is a finite field with q elements
    try:
        q_int = int(q)
        if q_int < 2:
            h1 = False
        else:
            factors = factorint(q_int)
            h1 = (len(factors) == 1)
    except Exception:
        h1 = False

    # H_2: The degree of f(x) is n >= 1
    try:
        f_expr = sympy.sympify(f)
        poly_f = Poly(f_expr, x)
        if poly_f.is_zero:
            n = -1
            h2 = False
        else:
            n = poly_f.degree()
            h2 = bool(n >= 1)
    except Exception:
        h2 = False
        n = -1

    # neg_Q: The factor ring of polynomials over F_q modulo f(x) does not have exactly q^n elements
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            p = list(factorint(q_int).keys())[0]
            poly_mod_p = Poly(f_expr, x, domain=sympy.GF(p))
            if poly_mod_p.is_zero:
                m = -1
            else:
                m = poly_mod_p.degree()
            neg_q = bool(m != n)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: The degree of f(x) is n >= 1",
    "¬Q: The factor ring of polynomials over F_q modulo f(x) does not have exactly q^n elements"
]

N_HYP = 2
NEG_Q_INDEX = 2
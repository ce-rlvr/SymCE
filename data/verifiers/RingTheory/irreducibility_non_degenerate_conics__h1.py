import sympy
from sympy.abc import x, y
from sympy import Poly, Matrix, factor_list
import sympy.combinatorics
import sympy.matrices

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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: f is a polynomial of degree at most 2",
    "H_2: The determinant of the symmetric matrix is non-zero",
    "not Q: f is reducible"
]

def conditions(witness):
    # H_1
    try:
        expr = sympy.sympify(witness)
        if not expr.free_symbols.issubset({x, y}):
            h1 = False
        else:
            p = Poly(expr, x, y)
            if p.total_degree() > 2:
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False

    # H_2
    try:
        expr = sympy.sympify(witness)
        p = Poly(expr, x, y)
        a = p.coeff_monomial(x**2)
        b = p.coeff_monomial(x*y)
        c = p.coeff_monomial(y**2)
        d = p.coeff_monomial(x)
        e = p.coeff_monomial(y)
        g = p.coeff_monomial(1)
        
        two = sympy.S(2)
        M = Matrix([
            [a, b/two, d/two],
            [b/two, c, e/two],
            [d/two, e/two, g]
        ])
        h2 = (M.det() != 0)
    except Exception:
        h2 = False

    # neg_Q
    try:
        expr = sympy.sympify(witness)
        p = Poly(expr, x, y)
        if p.is_zero or p.total_degree() <= 0:
            neg_q = False
        else:
            content, factors = factor_list(expr)
            non_constant_factors = sum(exp for base, exp in factors if Poly(base, x, y).total_degree() > 0)
            neg_q = (non_constant_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
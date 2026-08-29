import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy import Poly
from sympy.abc import x

# Standard group theory bindings
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

# Standard linear algebra bindings
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (f, g), checks if it is a valid counterexample to the false conjecture.
    f and g can be SymPy expressions, strings, or lists of coefficients.
    """
    try:
        f, g = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a Unique Factorization Domain
    try:
        poly_f = Poly(f, x)
        poly_g = Poly(g, x)
        domain = poly_f.domain.unify(poly_g.domain)
        poly_f = Poly(f, x, domain=domain)
        poly_g = Poly(g, x, domain=domain)
        h1 = bool(domain.is_UFD)
    except Exception:
        h1 = False

    # H_2: g is a primitive polynomial
    try:
        if h1:
            c_g = poly_g.content()
            h2 = bool(c_g == domain.one)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The product polynomial fg is not a primitive polynomial
    try:
        if h1:
            poly_fg = poly_f * poly_g
            c_fg = poly_fg.content()
            neg_q = bool(c_fg != domain.one)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: g is a primitive polynomial",
    "¬Q: The product polynomial fg is not a primitive polynomial"
]

N_HYP = 2
NEG_Q_INDEX = 2
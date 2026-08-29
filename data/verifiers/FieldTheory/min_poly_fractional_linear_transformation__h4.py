import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy import minpoly, degree, Rational, Integer
from sympy.abc import x
import math
import itertools
import functools

# Top-level setup
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
        n = None
        # Flexible unpacking to support various witness formats
        if len(witness) == 5:
            alpha, a, b, c, d = witness
        elif len(witness) == 6:
            if str(witness[0]) in ['Q', 'QQ', 'RationalField', 'QQ()']:
                F_val, alpha, a, b, c, d = witness
            else:
                alpha, n, a, b, c, d = witness
        elif len(witness) == 7:
            F_val, alpha, n, a, b, c, d = witness
        else:
            return [False, False, False, False]
            
        alpha = sympy.sympify(alpha)
        if n is not None:
            n = int(n)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        c = sympy.sympify(c)
        d = sympy.sympify(d)
    except Exception:
        return [False, False, False, False]

    # H1: alpha is algebraic over Q
    try:
        p_alpha = minpoly(alpha, x, domain=sympy.QQ)
        h1 = True
    except Exception:
        h1 = False
        p_alpha = None

    # H2: minpoly of alpha has degree n
    try:
        if h1:
            if n is None:
                n = degree(p_alpha, x)
                h2 = True
            else:
                h2 = bool(degree(p_alpha, x) == n)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: a, b, c, d in Q and ad - bc != 0
    try:
        h3 = bool(a.is_rational and b.is_rational and c.is_rational and d.is_rational and (a*d - b*c != 0))
    except Exception:
        h3 = False

    # neg_Q: minpoly of (a*alpha + b)/(c*alpha + d) does NOT have degree n
    try:
        denom = c*alpha + d
        if denom == 0:
            neg_q = True
        else:
            beta = (a*alpha + b) / denom
            p_beta = minpoly(beta, x, domain=sympy.QQ)
            neg_q = bool(degree(p_beta, x) != n)
    except Exception:
        # If minpoly fails (e.g. division by zero or not algebraic), it doesn't have degree n
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is algebraic over F",
    "H_2: The minimal polynomial of alpha over F has degree n",
    "H_3: a, b, c, d in F and ad - bc != 0",
    "¬Q: The minimal polynomial of (a*alpha + b)/(c*alpha + d) over F does NOT have degree n"
]

N_HYP = 3
NEG_Q_INDEX = 3
import sympy
from sympy import Poly, minpoly, simplify, sympify, eye, zeros, Eq
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z
import z3
import math
import itertools
import functools

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
    "H_1: E is an extension field of F",
    "H_2: alpha in E is an element algebraic over F",
    "H_3: p(x) is a monic polynomial over F",
    "H_4: p(x) is irreducible over F",
    "H_5: p(alpha) = 0",
    "¬Q: p(x) is not the minimal polynomial of alpha over F"
]

N_HYP = 5
NEG_Q_INDEX = 5

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            E = witness.get('E')
            alpha = witness.get('alpha')
            p_expr = witness.get('p')
            x_var = witness.get('x', x)
        else:
            if len(witness) == 5:
                F, E, alpha, p_expr, x_var = witness
            else:
                F, E, alpha, p_expr = witness
                x_var = x

        if isinstance(p_expr, Eq):
            p_expr = p_expr.lhs - p_expr.rhs
        elif isinstance(p_expr, Poly):
            p_expr = p_expr.as_expr()
        elif isinstance(p_expr, str):
            p_expr = sympify(p_expr)

        if isinstance(alpha, str):
            alpha = sympify(alpha)

        try:
            h1 = getattr(F, 'is_Field', False) and getattr(E, 'is_Field', False)
        except Exception:
            h1 = False

        try:
            in_E = alpha in E
        except Exception:
            in_E = False

        try:
            mp = minpoly(alpha, x_var, domain=F)
            is_alg = True
        except Exception:
            is_alg = False

        h2 = in_E and is_alg

        try:
            p = Poly(p_expr, x_var, domain=F)
            h3 = p.is_monic
        except Exception:
            h3 = False

        try:
            p = Poly(p_expr, x_var, domain=F)
            h4 = p.is_irreducible
        except Exception:
            h4 = False

        try:
            h5 = simplify(p_expr.subs(x_var, alpha)) == 0
        except Exception:
            h5 = False

        try:
            mp = minpoly(alpha, x_var, domain=F)
            mp_poly = Poly(mp, x_var, domain=F)
            p = Poly(p_expr, x_var, domain=F)
            neg_q = (p != mp_poly)
        except Exception:
            neg_q = False

        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]
    except Exception:
        return [False, False, False, False, False, False]
import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup for potential witness references
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
    "H_1: R is a Unique Factorization Domain",
    "H_2: u in R is a unit",
    "¬Q: The content of f(ux) is not associate to the content of f(x) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Extract witness components. Expected formats: (R, u, f, x) or (R, u, f)
    try:
        if len(witness) == 4:
            R, u, f, x = witness
        elif len(witness) == 3:
            R, u, f = witness
            x = symbols('x')
            if hasattr(f, 'free_symbols'):
                syms = list(f.free_symbols)
                if len(syms) == 1:
                    x = syms[0]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False

    # H_2: u in R is a unit
    try:
        u_sym = sympify(u)
        if u_sym in R:
            inv_u = cancel(1 / u_sym)
            h2 = bool(inv_u in R)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The content of f(ux) is not associate to the content of f(x) in R
    try:
        f_sym = sympify(f)
        x_sym = sympify(x)
        u_sym = sympify(u)
        
        def to_expr(c):
            if hasattr(c, 'as_expr'):
                return c.as_expr()
            return sympify(c)
            
        # Compute content of f(x)
        try:
            p1 = Poly(f_sym, x_sym, domain=R)
            c1 = p1.content()
        except Exception:
            # Fallback for non-polynomial expressions
            c1 = f_sym.as_content_primitive()[0]
            
        # Compute content of f(u*x)
        f_u = f_sym.subs(x_sym, u_sym * x_sym)
        try:
            p2 = Poly(f_u, x_sym, domain=R)
            c2 = p2.content()
        except Exception:
            c2 = f_u.as_content_primitive()[0]
            
        c1_sym = to_expr(c1)
        c2_sym = to_expr(c2)
        
        # Check if c1 and c2 are associate in R (i.e., they mutually divide each other)
        if c1_sym == 0 and c2_sym == 0:
            is_assoc = True
        elif c1_sym == 0 or c2_sym == 0:
            is_assoc = False
        else:
            div1 = cancel(c1_sym / c2_sym)
            div2 = cancel(c2_sym / c1_sym)
            is_assoc = bool((div1 in R) and (div2 in R))
            
        neg_q = not is_assoc
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
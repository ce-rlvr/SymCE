import sympy
from sympy import Poly, zeros, simplify, eye, factor_list, Matrix
from sympy.abc import x
import math
import itertools
import functools

# Top-level setup for standard objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        p_expr, C = witness
    except Exception:
        return [False, False]
    
    # H1: p(x) is a monic polynomial of degree n >= 1 and C is a square matrix
    try:
        p_poly = Poly(p_expr, x)
        h1 = (p_poly.LC() == 1) and (p_poly.degree() >= 1) and getattr(C, 'is_square', False)
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails
    try:
        cp = C.charpoly(x).as_expr()
        charpoly_match = (simplify(cp - p_expr) == 0)
        
        if not charpoly_match:
            q_holds = False
        else:
            q_holds = True
            # If charpoly matches, check if the minimal polynomial is strictly smaller.
            # It is strictly smaller iff a proper divisor of p(x) annihilates C.
            # We only need to check p(x) divided by each of its irreducible factors.
            factors = factor_list(p_expr)
            for f, mult in factors[1]:
                q_expr = simplify(p_expr / f)
                q_poly = Poly(q_expr, x)
                q_C = zeros(C.rows, C.cols)
                
                for deg, coeff in q_poly.as_dict().items():
                    q_C += coeff * (C ** deg[0])
                
                is_zero = True
                for e in q_C:
                    if simplify(e) != 0:
                        is_zero = False
                        break
                
                if is_zero:
                    q_holds = False
                    break
                    
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p(x) is a monic polynomial of degree n >= 1 and C is a square matrix",
    "¬Q: The characteristic polynomial, minimal polynomial, or eigenvalues of C do not match p(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1
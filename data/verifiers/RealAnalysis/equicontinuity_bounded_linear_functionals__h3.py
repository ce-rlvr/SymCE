import sympy
from sympy import symbols, Matrix, Rational, Float
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
n, m, k = symbols('n m k', integer=True)
x, y, z = symbols('x y z', real=True)
t = symbols('t', real=True)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False

    try:
        # Check H1: V is a finite-dimensional normed vector space over R
        if callable(witness):
            v = witness(1)
            if isinstance(v, sympy.MatrixBase):
                dim = len(v)
            elif isinstance(v, (list, tuple)):
                dim = len(v)
            else:
                dim = 1
            h1 = dim > 0
        elif isinstance(witness, tuple) and len(witness) == 2:
            expr, var = witness
            if isinstance(expr, sympy.MatrixBase):
                dim = len(expr)
            elif isinstance(expr, (list, tuple)):
                dim = len(expr)
            elif isinstance(expr, sympy.Expr):
                dim = 1
            else:
                dim = 0
            h1 = dim > 0
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        # Check H2: F is a family of continuous linear functionals on V
        def check_e(e, var=None):
            if not isinstance(e, sympy.Expr):
                return True
            if var is not None:
                syms = [s for s in e.free_symbols if s != var]
            else:
                syms = list(e.free_symbols)
            if not syms:
                return True
            try:
                poly = sympy.Poly(e, *syms)
                if poly.total_degree() > 1:
                    return False
                if sympy.simplify(e.subs({s: 0 for s in syms})) != 0:
                    return False
                return True
            except Exception:
                return False

        if isinstance(witness, tuple) and len(witness) == 2:
            expr, var = witness
            if isinstance(expr, sympy.MatrixBase) or isinstance(expr, (list, tuple)):
                h2 = all(check_e(e, var) for e in expr)
            else:
                h2 = check_e(expr, var)
        elif callable(witness):
            v = witness(1)
            if isinstance(v, sympy.MatrixBase) or isinstance(v, (list, tuple)):
                h2 = all(check_e(e) for e in v)
            else:
                h2 = check_e(v)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        # Check neg_Q: F is NOT uniformly equicontinuous on V
        # This is true iff the family is unbounded in operator norm.
        n_values = [10**i for i in range(15)]
        norms = []
        
        def get_norm_of_eval(v):
            norm = 0
            if isinstance(v, sympy.MatrixBase) or isinstance(v, (list, tuple)):
                for e in v:
                    if isinstance(e, sympy.Expr):
                        syms = list(e.free_symbols)
                        if syms:
                            poly = sympy.Poly(e, *syms)
                            norm += sum(abs(float(c)) for c in poly.coeffs())
                        else:
                            norm += abs(float(e))
                    else:
                        norm += abs(float(e))
            elif isinstance(v, sympy.Expr):
                syms = list(v.free_symbols)
                if syms:
                    poly = sympy.Poly(v, *syms)
                    norm += sum(abs(float(c)) for c in poly.coeffs())
                else:
                    norm += abs(float(v))
            else:
                norm += abs(float(v))
            return norm

        if callable(witness):
            for n_val in n_values:
                v = witness(n_val)
                norms.append(get_norm_of_eval(v))
        elif isinstance(witness, tuple) and len(witness) == 2:
            expr, var = witness
            for n_val in n_values:
                if isinstance(expr, sympy.MatrixBase) or isinstance(expr, (list, tuple)):
                    v = [e.subs(var, n_val) if isinstance(e, sympy.Expr) else e for e in expr]
                elif isinstance(expr, sympy.Expr):
                    v = expr.subs(var, n_val)
                else:
                    v = expr
                norms.append(get_norm_of_eval(v))
                
        if norms:
            max_norm = max(norms)
            if max_norm > 1e5:
                neg_q = True
            else:
                is_growing = True
                for i in range(1, 6):
                    if len(norms) >= i + 1:
                        if norms[-i] <= norms[-i-1] + 1e-7:
                            is_growing = False
                            break
                    else:
                        is_growing = False
                        break
                if is_growing and max_norm > norms[0] + 1:
                    neg_q = True
                else:
                    neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional normed vector space over R",
    "H_2: F is a family of continuous linear functionals on V",
    "¬Q: F is not uniformly equicontinuous on V"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
import math
import itertools
import functools
from sympy.abc import a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f and g are polynomials over R",
    "¬Q: The content ideal c(fg) is not contained in the product ideal c(f)c(g)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            vars_ = witness.get('vars', [])
            I = witness.get('I', [])
            x_var = witness.get('x', None)
            f_poly_expr = witness.get('f', None)
            g_poly_expr = witness.get('g', None)
        elif isinstance(witness, tuple):
            if len(witness) == 5:
                vars_, I, x_var, f_poly_expr, g_poly_expr = witness
            elif len(witness) == 4:
                vars_, x_var, f_poly_expr, g_poly_expr = witness
                I = []
            elif len(witness) == 3:
                x_var, f_poly_expr, g_poly_expr = witness
                vars_ = []
                I = []
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if isinstance(vars_, (list, tuple)):
            vars_ = [sympy.Symbol(v) if isinstance(v, str) else v for v in vars_]
            
        if isinstance(f_poly_expr, str):
            f_poly_expr = sympy.sympify(f_poly_expr)
        if isinstance(g_poly_expr, str):
            g_poly_expr = sympy.sympify(g_poly_expr)
            
        if isinstance(I, (list, tuple)):
            I_exprs = []
            for expr in I:
                if isinstance(expr, str):
                    expr = sympy.sympify(expr)
                if hasattr(expr, 'lhs') and hasattr(expr, 'rhs'):
                    I_exprs.append(expr.lhs - expr.rhs)
                else:
                    I_exprs.append(expr)
            I = I_exprs
            
        if isinstance(x_var, str):
            x_var = sympy.Symbol(x_var)
            
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring with identity
    try:
        h1 = isinstance(vars_, (list, tuple)) and all(hasattr(v, 'is_Symbol') for v in vars_)
        h1 = h1 and isinstance(I, (list, tuple))
    except Exception:
        h1 = False

    # H2: f and g are polynomials over R
    try:
        if not h1 or x_var is None or f_poly_expr is None or g_poly_expr is None:
            h2 = False
        else:
            f_poly = sympy.Poly(f_poly_expr, x_var)
            g_poly = sympy.Poly(g_poly_expr, x_var)
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: c(f)c(g) is not contained in c(fg) (or vice versa)
    try:
        if not h2:
            neg_q = False
        else:
            fg_poly = sympy.Poly(f_poly_expr * g_poly_expr, x_var)
            
            c_f = f_poly.coeffs()
            c_g = g_poly.coeffs()
            c_fg = fg_poly.coeffs()
            
            all_syms = set()
            if hasattr(f_poly_expr, 'free_symbols'):
                all_syms |= f_poly_expr.free_symbols
            if hasattr(g_poly_expr, 'free_symbols'):
                all_syms |= g_poly_expr.free_symbols
            for expr in I:
                if hasattr(expr, 'free_symbols'):
                    all_syms |= expr.free_symbols
            if x_var in all_syms:
                all_syms.remove(x_var)
                
            gb_vars = list(set(vars_) | all_syms)
            
            if not gb_vars:
                neg_q = False
            else:
                # Check if c(f)c(g) is contained in c(fg)
                gb_cfg = sympy.groebner(list(c_fg) + list(I), *gb_vars)
                cfcg_in_cfg = True
                for a_coeff in c_f:
                    for b_coeff in c_g:
                        prod = a_coeff * b_coeff
                        rem = sympy.reduced(prod, gb_cfg, *gb_vars)[1]
                        if sympy.simplify(rem) != 0:
                            cfcg_in_cfg = False
                            break
                    if not cfcg_in_cfg:
                        break
                
                # Check if c(fg) is contained in c(f)c(g)
                cfcg_generators = [a_coeff * b_coeff for a_coeff in c_f for b_coeff in c_g] + list(I)
                gb_cfcg = sympy.groebner(cfcg_generators, *gb_vars)
                cfg_in_cfcg = True
                for coeff in c_fg:
                    rem = sympy.reduced(coeff, gb_cfcg, *gb_vars)[1]
                    if sympy.simplify(rem) != 0:
                        cfg_in_cfcg = False
                        break
                
                neg_q = not (cfcg_in_cfg and cfg_in_cfcg)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]
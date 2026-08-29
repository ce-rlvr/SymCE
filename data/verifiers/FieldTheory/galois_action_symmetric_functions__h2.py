import sympy
from sympy import symbols, Poly

x = symbols('x')
x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = symbols('x1:11')

def conditions(witness):
    try:
        f_expr, alphas, S_expr = witness
        f_expr = sympy.sympify(f_expr)
        alphas = [sympy.sympify(a) for a in alphas]
        S_expr = sympy.sympify(S_expr)
    except Exception:
        return [False, False, False, False]
        
    try:
        f_poly = Poly(f_expr, x, domain='QQ')
        h1 = f_poly.is_sqf
    except Exception:
        h1 = False
        
    try:
        if not alphas:
            h2 = False
        else:
            alphas_are_roots = all(sympy.simplify(f_expr.subs(x, a)) == 0 for a in alphas)
            unique = []
            for a in alphas:
                if not any(sympy.simplify(a - u) == 0 for u in unique):
                    unique.append(a)
            h2 = alphas_are_roots and len(unique) == len(alphas)
    except Exception:
        h2 = False
        
    try:
        n = len(alphas)
        xs = symbols(f'x1:{n+1}')
        if isinstance(xs, sympy.Symbol):
            xs = (xs,)
        S_poly = Poly(S_expr, xs, domain='QQ')
        if not S_expr.free_symbols.issubset(set(xs)):
            h3 = False
        else:
            is_symmetric = True
            if n > 1:
                for i in range(n - 1):
                    swapped_xs = list(xs)
                    swapped_xs[i], swapped_xs[i+1] = swapped_xs[i+1], swapped_xs[i]
                    S_swapped = S_expr.subs(zip(xs, swapped_xs))
                    if sympy.simplify(S_expr - S_swapped) != 0:
                        is_symmetric = False
                        break
            h3 = is_symmetric
    except Exception:
        h3 = False
        
    try:
        n = len(alphas)
        xs = symbols(f'x1:{n+1}')
        if isinstance(xs, sympy.Symbol):
            xs = (xs,)
        S_val = S_expr.subs(zip(xs, alphas))
        S_val_simp = sympy.simplify(S_val)
        
        in_K = S_val_simp.is_Rational
        if in_K is None:
            try:
                sympy.Rational(S_val_simp)
                in_K = True
            except TypeError:
                in_K = False
                
        neg_Q = not in_K
    except Exception:
        neg_Q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: f(x) is separable",
    "H_2: alphas are roots of f(x)",
    "H_3: S is symmetric",
    "¬Q: S(alphas) not in K"
]

N_HYP = 3
NEG_Q_INDEX = 3
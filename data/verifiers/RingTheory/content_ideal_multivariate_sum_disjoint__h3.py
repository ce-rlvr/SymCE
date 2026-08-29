import sympy
from sympy import Symbol, Expr, Poly, gcd
from functools import reduce

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z, t, u, v = sympy.symbols('x y z t u v')

def conditions(witness):
    try:
        X, Y, f, g = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        X_set = set(X)
        Y_set = set(Y)
    except Exception:
        X_set = set()
        Y_set = set()

    # H1: R is a commutative ring
    try:
        h1 = isinstance(f, (Expr, int, float)) and isinstance(g, (Expr, int, float))
    except Exception:
        h1 = False

    # H2: X and Y are disjoint sets of indeterminates over R
    try:
        if not isinstance(X, (set, list, tuple)) or not isinstance(Y, (set, list, tuple)):
            h2 = False
        else:
            h2 = all(isinstance(var, Symbol) for var in X_set | Y_set) and X_set.isdisjoint(Y_set)
    except Exception:
        h2 = False

    # H3: g is a polynomial in Y over R
    try:
        g_expr = sympy.sympify(g)
        g_syms = g_expr.free_symbols
        if not g_syms.issubset(Y_set):
            h3 = False
        else:
            if Y_set:
                p_g = Poly(g_expr, *list(Y_set))
            h3 = True
    except Exception:
        h3 = False

    # H4: The constant term of f is zero
    try:
        f_expr = sympy.sympify(f)
        vars_all = list(X_set | Y_set)
        if vars_all:
            const_term = f_expr.subs({var: 0 for var in vars_all})
        else:
            const_term = f_expr
        h4 = (sympy.simplify(const_term) == 0)
    except Exception:
        h4 = False

    # neg_Q: c(f+g) != c(f) + c(g)
    try:
        f_expr = sympy.sympify(f)
        g_expr = sympy.sympify(g)
        vars_all = list(X_set | Y_set)
        
        def content(expr):
            if not vars_all:
                return expr
            try:
                p = Poly(expr, *vars_all)
                coeffs = p.coeffs()
                if not coeffs:
                    return 0
                return reduce(gcd, coeffs)
            except Exception:
                return 0
                
        c_f = content(f_expr)
        c_g = content(g_expr)
        c_fg = content(f_expr + g_expr)
        
        c_f_plus_g = gcd(c_f, c_g)
        
        diff1 = sympy.simplify(c_fg - c_f_plus_g)
        diff2 = sympy.simplify(c_fg + c_f_plus_g)
        neg_q = (diff1 != 0) and (diff2 != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: X and Y are disjoint sets of indeterminates over R",
    "H_3: g is a polynomial in Y over R",
    "H_4: The constant term of f is zero",
    "¬Q: c(f+g) != c(f) + c(g)"
]

N_HYP = 4
NEG_Q_INDEX = 4
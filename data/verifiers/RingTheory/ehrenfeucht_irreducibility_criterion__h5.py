import sympy
import math

x, y, z, t = sympy.symbols('x y z t')
QQ = sympy.QQ
ZZ = sympy.ZZ
RR = sympy.RR
CC = sympy.CC

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            K = witness.get('K')
            f = witness.get('f')
            g = witness.get('g')
            x_sym = witness.get('x', sympy.Symbol('x'))
            y_sym = witness.get('y', sympy.Symbol('y'))
        elif isinstance(witness, tuple):
            if len(witness) == 5:
                K, f, g, x_sym, y_sym = witness
            elif len(witness) == 3:
                K, f, g = witness
                f_expr = sympy.sympify(f)
                g_expr = sympy.sympify(g)
                free_f = f_expr.free_symbols
                free_g = g_expr.free_symbols
                x_sym = list(free_f)[0] if free_f else sympy.Symbol('x')
                y_sym = list(free_g)[0] if free_g else sympy.Symbol('y')
            else:
                return [False] * 6
        else:
            return [False] * 6
    except Exception:
        return [False] * 6

    try:
        h1 = bool(getattr(K, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        f_expr = sympy.sympify(f)
        f_poly = sympy.Poly(f_expr, x_sym, domain=K)
        if any(sym != x_sym for sym in f_expr.free_symbols):
            h2 = False
        else:
            h2 = True
    except Exception:
        h2 = False

    try:
        g_expr = sympy.sympify(g)
        g_poly = sympy.Poly(g_expr, y_sym, domain=K)
        if any(sym != y_sym for sym in g_expr.free_symbols):
            h3 = False
        else:
            h3 = True
    except Exception:
        h3 = False

    try:
        df = f_poly.degree()
        h4 = bool(df >= 1)
    except Exception:
        h4 = False

    try:
        dg = g_poly.degree()
        if df == -sympy.oo or dg == -sympy.oo:
            h5 = False
        else:
            h5 = bool(math.gcd(int(df), int(dg)) == 1)
    except Exception:
        h5 = False

    try:
        F = f_expr - g_expr
        if F == 0:
            neg_q = True
        else:
            gens = []
            for gen in (x_sym, y_sym):
                if gen not in gens:
                    gens.append(gen)
            
            factors = sympy.factor_list(F, *gens, domain=K)
            num_factors = sum(exp for fac, exp in factors[1])
            neg_q = bool(num_factors != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is a polynomial over K",
    "H_3: g is a polynomial over K",
    "H_4: deg(f) >= 1",
    "H_5: gcd(deg(f), deg(g)) == 1",
    "not Q: f - g is reducible"
]

N_HYP = 5
NEG_Q_INDEX = 5
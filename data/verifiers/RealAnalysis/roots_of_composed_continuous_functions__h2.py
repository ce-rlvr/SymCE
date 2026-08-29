import sympy
import z3

# Top-level setup
x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    """
    try:
        a = float(witness['a'])
        b = float(witness['b'])
        c = float(witness['c'])
        d = float(witness['d'])
    except Exception:
        return [False] * 4 + [False]

    def get_callable(name):
        if f"{name}_coeffs" in witness:
            coeffs = witness[f"{name}_coeffs"]
            def poly(val):
                if not coeffs:
                    return val * 0
                res = coeffs[0]
                p = val
                for coef in coeffs[1:]:
                    res = res + coef * p
                    p = p * val
                return res
            return poly
        elif name in witness:
            obj = witness[name]
            if callable(obj):
                return obj
            elif isinstance(obj, sympy.Expr):
                free_syms = list(obj.free_symbols)
                sym = free_syms[0] if free_syms else sympy.Symbol('x', real=True)
                try:
                    poly_obj = sympy.Poly(obj, sym)
                    coeffs = poly_obj.all_coeffs()[::-1]
                    def poly_func(val):
                        if not coeffs:
                            return val * 0
                        res = float(coeffs[0])
                        p = val
                        for coef in coeffs[1:]:
                            res = res + float(coef) * p
                            p = p * val
                        return res
                    return poly_func
                except Exception:
                    def fallback(val):
                        if z3.is_expr(val):
                            raise ValueError("Cannot evaluate non-poly with z3")
                        return float(obj.subs(sym, val))
                    return fallback
        return None

    f = get_callable('f')
    g = get_callable('g')

    if f is None or g is None:
        return [False] * 4 + [False]

    # H1: f is a continuous function from [a,b] to [c,d]
    try:
        h1_ok = False
        if a < b and c < d:
            zx = z3.Real('x')
            f_x = f(zx)
            if isinstance(f_x, (int, float)):
                f_x = z3.RealVal(f_x)
            
            solver = z3.Solver()
            solver.set("timeout", 2000)
            solver.add(zx >= a, zx <= b)
            solver.add(z3.Or(f_x < c, f_x > d))
            if solver.check() == z3.unsat:
                h1_ok = True
    except Exception:
        h1_ok = False

    # H2: g is a continuous function from [c,d] to R
    try:
        h2_ok = False
        if c < d:
            zx = z3.Real('x')
            g_x = g(zx)
            if isinstance(g_x, (int, float)):
                g_x = z3.RealVal(g_x)
            h2_ok = True
    except Exception:
        h2_ok = False

    # H3: g(c) < 0
    try:
        gc = g(c)
        if z3.is_expr(gc):
            solver = z3.Solver()
            solver.set("timeout", 1000)
            solver.add(gc >= 0)
            h3_ok = (solver.check() == z3.unsat)
        else:
            h3_ok = bool(gc < 0)
    except Exception:
        h3_ok = False

    # H4: g(d) > 0
    try:
        gd = g(d)
        if z3.is_expr(gd):
            solver = z3.Solver()
            solver.set("timeout", 1000)
            solver.add(gd <= 0)
            h4_ok = (solver.check() == z3.unsat)
        else:
            h4_ok = bool(gd > 0)
    except Exception:
        h4_ok = False

    # neg_Q: For all x in [a,b], g(f(x)) != 0
    try:
        neg_q_ok = False
        zx = z3.Real('x')
        f_x = f(zx)
        if isinstance(f_x, (int, float)):
            f_x = z3.RealVal(f_x)
        g_f_x = g(f_x)
        if isinstance(g_f_x, (int, float)):
            g_f_x = z3.RealVal(g_f_x)
        
        solver = z3.Solver()
        solver.set("timeout", 2000)
        solver.add(zx >= a, zx <= b)
        solver.add(g_f_x == 0)
        if solver.check() == z3.unsat:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a continuous function from interval a to b to interval c to d",
    "H_2: g is a continuous function from interval c to d to R",
    "H_3: g(c) < 0",
    "H_4: g(d) > 0",
    "¬Q: For all x in interval a to b, g(f(x)) != 0"
]

N_HYP = 4
NEG_Q_INDEX = 4
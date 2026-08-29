import sympy

x = sympy.Symbol('x', real=True)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            a = witness.get('a')
            b = witness.get('b')
        else:
            f, a, b = witness

        a = sympy.sympify(a)
        b = sympy.sympify(b)

        if not a.is_real or not b.is_real:
            return [False, False, False]
            
        if not bool(a < b):
            return [False, False, False]

        if callable(f):
            f_expr = f(x)
            sym = x
        else:
            f_expr = sympy.sympify(f)
            free_syms = f_expr.free_symbols
            if len(free_syms) >= 1:
                if x in free_syms:
                    sym = x
                else:
                    sym = list(free_syms)[0]
            else:
                sym = x

        # H1: f is continuous on the interval
        try:
            if hasattr(sympy, 'continuous_domain'):
                domain = sympy.continuous_domain(f_expr, sym, sympy.S.Reals)
                h1 = bool(sympy.Interval(a, b).is_subset(domain))
            else:
                h1 = True
                den = sympy.denom(f_expr)
                if den != 1:
                    poles = sympy.solveset(den, sym, domain=sympy.Interval(a, b))
                    if not poles.is_empty:
                        h1 = False
                
                if h1:
                    for i in range(101):
                        val = a + (b - a) * i / 100
                        v = f_expr.subs(sym, val)
                        if not v.is_real or v.has(sympy.oo, sympy.zoo, -sympy.oo):
                            h1 = False
                            break
        except Exception:
            h1 = False

        # H2: f(b) <= b
        try:
            fb = f_expr.subs(sym, b)
            h2 = bool(fb <= b)
        except Exception:
            h2 = False

        # neg_Q: no c in the interval such that f(c) = c
        try:
            sols = sympy.solveset(f_expr - sym, sym, domain=sympy.Interval(a, b))
            if sols is sympy.S.EmptySet:
                neg_q = True
            elif isinstance(sols, sympy.FiniteSet) and len(sols) > 0:
                neg_q = False
            else:
                neg_q = True
                vals = []
                for i in range(101):
                    val = a + (b - a) * i / 100
                    v = (f_expr - sym).subs(sym, val)
                    if v.is_real and not v.has(sympy.oo, sympy.zoo, -sympy.oo):
                        vals.append(float(v))
                if len(vals) > 0:
                    if max(vals) >= 0 and min(vals) <= 0:
                        neg_q = False
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f is a continuous function",
    "H_2: f(b) <= b",
    "¬Q: There is no c such that f(c) = c"
]

N_HYP = 2
NEG_Q_INDEX = 2
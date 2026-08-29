import sympy
from sympy import Poly, gcd, cancel, fraction
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: f and g are non-zero polynomials",
    "H_2: The sum f + g is a non-zero polynomial",
    "not Q: gcd of contents does not divide content of sum"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                f_expr, g_expr, gen = witness
                f = f_expr if isinstance(f_expr, Poly) else Poly(f_expr, gen)
                g = g_expr if isinstance(g_expr, Poly) else Poly(g_expr, gen)
            elif len(witness) == 2:
                f_expr, g_expr = witness
                if isinstance(f_expr, Poly) and isinstance(g_expr, Poly):
                    f = f_expr
                    g = g_expr
                else:
                    f = Poly(f_expr, x)
                    g = Poly(g_expr, x)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1_ok = not f.is_zero and not g.is_zero
    except Exception:
        h1_ok = False

    try:
        fg = f + g
        h2_ok = not fg.is_zero
    except Exception:
        h2_ok = False

    try:
        cf = f.content()
        cg = g.content()
        cfg = fg.content()
        
        domain = fg.domain
        d = domain.gcd(cf, cg)
        
        if d == domain.zero:
            q_holds = (cfg == domain.zero)
        else:
            try:
                domain.exquo(cfg, d)
                q_holds = True
            except Exception:
                try:
                    ratio = cancel(cfg / d)
                    num, den = fraction(ratio)
                    q_holds = (den == 1 or den == -1)
                except Exception:
                    q_holds = False
    except Exception:
        try:
            cf = f.content()
            cg = g.content()
            cfg = fg.content()
            d = gcd(cf, cg)
            
            if d == 0:
                q_holds = (cfg == 0)
            else:
                ratio = cancel(cfg / d)
                num, den = fraction(ratio)
                q_holds = (den == 1 or den == -1)
        except Exception:
            q_holds = True

    neg_q_ok = not q_holds

    return [h1_ok, h2_ok, neg_q_ok]
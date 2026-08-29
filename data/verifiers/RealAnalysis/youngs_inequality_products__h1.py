import sympy as sp
from sympy import eye, zeros
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f and g are measurable functions",
    "H_2: p > 1, q > 1, and 1/p + 1/q = 1",
    "H_3: |f|^p and |g|^q are Lebesgue integrable on Omega",
    "¬Q: Integral of |fg| is strictly greater than 1/p * Integral of |f|^p + 1/q * Integral of |g|^q"
]

N_HYP = 3
NEG_Q_INDEX = 3

def compute_integral(expr, vars_limits):
    res = expr
    for limit in vars_limits:
        res = sp.integrate(res, limit)
    if isinstance(res, sp.Integral) or res.has(sp.Integral):
        res = res.evalf()
    return res

def conditions(witness) -> list[bool]:
    # Check for discrete case first (e.g., vectors/sequences)
    if isinstance(witness, dict):
        f_val = witness.get('f')
        if isinstance(f_val, (list, tuple)) or (hasattr(f_val, 'is_Matrix') and f_val.is_Matrix):
            try:
                if hasattr(f_val, 'is_Matrix') and f_val.is_Matrix:
                    f = list(f_val)
                    g = list(witness['g'])
                else:
                    f = witness['f']
                    g = witness['g']
                p = float(sp.sympify(witness['p']))
                q = float(sp.sympify(witness['q']))
                
                h1 = True
                h2 = (p > 1) and (q > 1) and abs(1/p + 1/q - 1.0) < 1e-9
                
                sum_f_p = sum(abs(complex(x))**p for x in f)
                sum_g_q = sum(abs(complex(x))**q for x in g)
                h3 = True
                
                sum_fg = sum(abs(complex(x * y)) for x, y in zip(f, g))
                lhs = sum_fg
                rhs = (1/p) * sum_f_p + (1/q) * sum_g_q
                neg_q = lhs > rhs + 1e-9
                
                return [h1, h2, h3, neg_q]
            except Exception:
                pass # fall back to continuous case if it fails

    # Continuous case
    try:
        if isinstance(witness, dict):
            f = sp.sympify(witness['f'])
            g = sp.sympify(witness['g'])
            p = sp.sympify(witness['p'])
            q = sp.sympify(witness['q'])
            if 'vars_limits' in witness:
                vars_limits = witness['vars_limits']
            else:
                x = sp.sympify(witness.get('x', 'x'))
                domain = witness['domain']
                if isinstance(domain, tuple) and len(domain) == 2 and not isinstance(domain[0], tuple):
                    vars_limits = [(x, sp.sympify(domain[0]), sp.sympify(domain[1]))]
                else:
                    vars_limits = domain
        else:
            f, g, p, q, x, domain = witness
            f = sp.sympify(f)
            g = sp.sympify(g)
            p = sp.sympify(p)
            q = sp.sympify(q)
            x = sp.sympify(x)
            vars_limits = [(x, sp.sympify(domain[0]), sp.sympify(domain[1]))]
    except Exception:
        return [False, False, False, False]

    # H1: f and g are measurable
    try:
        h1 = isinstance(f, sp.Expr) and isinstance(g, sp.Expr)
    except Exception:
        h1 = False

    # H2: p > 1, q > 1, 1/p + 1/q = 1
    try:
        p_val = float(p)
        q_val = float(q)
        p_gt_1 = p_val > 1
        q_gt_1 = q_val > 1
        eq_check = abs(1/p_val + 1/q_val - 1.0) < 1e-9
        h2 = p_gt_1 and q_gt_1 and eq_check
    except Exception:
        h2 = False

    # H3: |f|^p and |g|^q are Lebesgue integrable
    try:
        expr_f_p = sp.Abs(f)**p
        expr_g_q = sp.Abs(g)**q
        
        int_f_p = compute_integral(expr_f_p, vars_limits)
        int_g_q = compute_integral(expr_g_q, vars_limits)
        
        h3 = True
        if int_f_p.has(sp.oo, -sp.oo, sp.zoo, sp.nan) or int_g_q.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
            h3 = False
        else:
            val_f = complex(int_f_p)
            val_g = complex(int_g_q)
            if abs(val_f.imag) > 1e-7 or abs(val_g.imag) > 1e-7:
                h3 = False
    except Exception:
        h3 = False

    # neg_Q: \int |fg| > 1/p \int |f|^p + 1/q \int |g|^q
    try:
        expr_fg = sp.Abs(f * g)
        int_fg = compute_integral(expr_fg, vars_limits)
        
        lhs = float(sp.re(int_fg))
        rhs = float(sp.re((1/p_val) * int_f_p + (1/q_val) * int_g_q))
        
        neg_q = lhs > rhs + 1e-9
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]
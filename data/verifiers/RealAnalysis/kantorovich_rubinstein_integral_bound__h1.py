import sympy
import math

x = sympy.Symbol('x')

CONDITION_LABELS = [
    "H_1: g and h are non-negative continuous functions",
    "H_2: integrals of g and h are 1",
    "H_3: G and H are cumulative integrals of g and h",
    "not Q: conclusion fails"
]
N_HYP = 3
NEG_Q_INDEX = 3

def num_int_lambdified(func, a_val, b_val, n=100):
    if abs(b_val - a_val) < 1e-12:
        return 0.0
    h_step = (b_val - a_val) / n
    s = func(a_val) + func(b_val)
    for i in range(1, n, 2):
        s += 4 * func(a_val + i * h_step)
    for i in range(2, n-1, 2):
        s += 2 * func(a_val + i * h_step)
    return s * h_step / 3.0

def conditions(witness):
    try:
        f = witness['f']
        g = witness['g']
        h = witness['h']
        a = float(witness['a'])
        b = float(witness['b'])
        L = float(witness['L'])
        if a >= b:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def make_func(expr):
        func = sympy.lambdify(x, expr, 'math')
        try:
            func((a + b) / 2.0)
            return func
        except Exception:
            return lambda val: float(expr.subs(x, val))

    # H1: g and h are non-negative, continuous real-valued functions
    try:
        h1_ok = True
        g_func = make_func(g)
        h_func = make_func(h)
        
        for i in range(101):
            val = a + (b - a) * i / 100.0
            if g_func(val) < -1e-5 or h_func(val) < -1e-5:
                h1_ok = False
                break
                
        # Check continuity using sympy
        from sympy.calculus.util import continuous_domain
        from sympy import Interval
        domain = Interval(a, b)
        if continuous_domain(g, x, domain) != domain:
            h1_ok = False
        if continuous_domain(h, x, domain) != domain:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H2: int_a^b g(x) dx = 1 and int_a^b h(x) dx = 1
    try:
        int_g_num = num_int_lambdified(g_func, a, b, n=500)
        int_h_num = num_int_lambdified(h_func, a, b, n=500)
        h2_ok = abs(int_g_num - 1.0) < 1e-4 and abs(int_h_num - 1.0) < 1e-4
    except Exception:
        h2_ok = False

    # H3: G(x) = int_a^x g(t) dt and H(x) = int_a^x h(t) dt
    try:
        if 'G' in witness and 'H' in witness:
            G_wit = witness['G']
            H_wit = witness['H']
            G_wit_func = make_func(G_wit)
            H_wit_func = make_func(H_wit)
            
            h3_ok = True
            for i in range(11):
                val = a + (b - a) * i / 10.0
                G_calc = num_int_lambdified(g_func, a, val, n=100)
                H_calc = num_int_lambdified(h_func, a, val, n=100)
                if abs(G_calc - G_wit_func(val)) > 1e-3 or abs(H_calc - H_wit_func(val)) > 1e-3:
                    h3_ok = False
                    break
        else:
            h3_ok = True
    except Exception:
        h3_ok = False

    # neg_Q: |int f*g - int f*h| > L * int |G - H|
    try:
        f_func = make_func(f)
        fg_func = lambda val: f_func(val) * g_func(val)
        fh_func = lambda val: f_func(val) * h_func(val)
        
        int_fg = num_int_lambdified(fg_func, a, b, n=500)
        int_fh = num_int_lambdified(fh_func, a, b, n=500)
        lhs = abs(int_fg - int_fh)
        
        if 'G' in witness and 'H' in witness:
            G_func = make_func(witness['G'])
            H_func = make_func(witness['H'])
            diff_GH_func = lambda val: abs(G_func(val) - H_func(val))
        else:
            def diff_GH_func(val):
                G_val = num_int_lambdified(g_func, a, val, n=100)
                H_val = num_int_lambdified(h_func, a, val, n=100)
                return abs(G_val - H_val)
                
        rhs_integral = num_int_lambdified(diff_GH_func, a, b, n=500)
        rhs = L * rhs_integral
        
        neg_q = lhs > rhs + 1e-7
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]
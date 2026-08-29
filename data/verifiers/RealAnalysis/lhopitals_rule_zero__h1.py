import sympy as sp
from sympy.abc import x, y, z, t
from sympy import Rational, Integer, oo, pi, E

def get_val(witness, prop):
    if isinstance(witness, dict):
        return witness.get(prop)
    return getattr(witness, prop, None)

def parse_expr(expr):
    if isinstance(expr, str):
        return sp.sympify(expr)
    return expr

def conditions(witness):
    try:
        f = parse_expr(get_val(witness, 'f'))
        g = parse_expr(get_val(witness, 'g'))
        
        x_sym = get_val(witness, 'x')
        if x_sym is not None:
            x_sym = parse_expr(x_sym)
        else:
            free_symbols = set()
            if hasattr(f, 'free_symbols'):
                free_symbols.update(f.free_symbols)
            if hasattr(g, 'free_symbols'):
                free_symbols.update(g.free_symbols)
            if free_symbols:
                x_sym = list(free_symbols)[0]
            else:
                x_sym = sp.Symbol('x')
                
        c = parse_expr(get_val(witness, 'c'))
        L = parse_expr(get_val(witness, 'L'))
        
        # H1: lim_{x -> c} f(x) = 0 and lim_{x -> c} g(x) = 0
        try:
            lim_f = sp.limit(f, x_sym, c)
            lim_g = sp.limit(g, x_sym, c)
            h1 = (sp.simplify(lim_f) == 0) and (sp.simplify(lim_g) == 0)
        except Exception:
            h1 = False
            
        # H2: g'(x) != 0 for all x in I \ {c}
        try:
            g_prime = get_val(witness, 'g_prime')
            if g_prime is not None:
                g_prime = parse_expr(g_prime)
            else:
                g_prime = sp.diff(g, x_sym)
                
            I_val = get_val(witness, 'I')
            if I_val is not None:
                if isinstance(I_val, (tuple, list)):
                    I_set = sp.Interval(parse_expr(I_val[0]), parse_expr(I_val[1]))
                else:
                    I_set = parse_expr(I_val)
                sols = sp.solveset(g_prime, x_sym, domain=sp.S.Reals)
                I_minus_c = sp.Intersection(I_set, sp.Complement(sp.S.Reals, sp.FiniteSet(c)))
                inter = sp.Intersection(sols, I_minus_c)
                if inter.is_empty == True:
                    h2 = True
                else:
                    h2 = False
            else:
                sols = sp.solveset(g_prime, x_sym, domain=sp.S.Reals)
                if sols.is_empty == True:
                    h2 = True
                elif isinstance(sols, sp.FiniteSet):
                    h2 = True
                else:
                    h2 = False
        except Exception:
            h2 = False
            
        # H3: The limit lim_{x -> c} f'(x)/g'(x) exists and equals L
        try:
            f_prime = get_val(witness, 'f_prime')
            if f_prime is not None:
                f_prime = parse_expr(f_prime)
            else:
                f_prime = sp.diff(f, x_sym)
            
            lim_fg_prime = sp.limit(f_prime / g_prime, x_sym, c)
            if L == sp.oo or L == -sp.oo:
                h3 = (lim_fg_prime == L)
            else:
                h3 = (sp.simplify(lim_fg_prime - L) == 0)
        except Exception:
            h3 = False
            
        # neg_Q: The limit lim_{x -> c} f(x)/g(x) does not exist or is not equal to L
        try:
            lim_fg = sp.limit(f / g, x_sym, c)
            if L == sp.oo or L == -sp.oo:
                neg_q = (lim_fg != L)
            else:
                diff = sp.simplify(lim_fg - L)
                neg_q = (diff != 0)
                if isinstance(neg_q, sp.Basic):
                    neg_q = True
        except Exception:
            neg_q = True
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: lim_{x -> c} f(x) = 0 and lim_{x -> c} g(x) = 0",
    "H_2: g'(x) != 0 for all x in I \\ {c}",
    "H_3: The limit lim_{x -> c} f'(x)/g'(x) exists and equals L",
    "¬Q: The limit lim_{x -> c} f(x)/g(x) does not exist or is not equal to L"
]

N_HYP = 3
NEG_Q_INDEX = 3
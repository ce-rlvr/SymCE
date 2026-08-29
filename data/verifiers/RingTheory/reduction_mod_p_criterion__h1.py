import sympy
import math

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n', 0)
            p_val = witness.get('p', 0)
            f_expr = witness.get('f', None)
            g_expr = witness.get('g', None)
            h_expr = witness.get('h', None)
        elif len(witness) == 5:
            n, p_val, f_expr, g_expr, h_expr = witness
        elif len(witness) == 4:
            n = 0
            p_val, f_expr, g_expr, h_expr = witness
        else:
            return [False] * 5
            
        n = abs(int(n))
        p_val = abs(int(p_val))
    except Exception:
        return [False] * 5

    def get_g():
        return math.gcd(p_val, n) if n > 0 else p_val

    def poly_degree(expr):
        try:
            p = sympy.Poly(expr, x)
            coeffs = p.all_coeffs()
            int_coeffs = []
            for c in coeffs:
                if not c.is_integer:
                    return -1
                int_coeffs.append(int(c))
            if n > 0:
                int_coeffs = [c % n for c in int_coeffs]
            for i, c in enumerate(int_coeffs):
                if c != 0:
                    return len(int_coeffs) - 1 - i
            return -1
        except Exception:
            return -1

    def get_lc(expr):
        try:
            p = sympy.Poly(expr, x)
            coeffs = p.all_coeffs()
            int_coeffs = []
            for c in coeffs:
                if not c.is_integer:
                    return 0
                int_coeffs.append(int(c))
            if n > 0:
                int_coeffs = [c % n for c in int_coeffs]
            for c in int_coeffs:
                if c != 0:
                    return c
            return 0
        except Exception:
            return 0

    try:
        g = get_g()
        if g == 0:
            h1 = True
        else:
            h1 = sympy.isprime(g)
    except Exception:
        h1 = False

    try:
        deg_f = poly_degree(f_expr)
        h2 = deg_f > 0
    except Exception:
        h2 = False

    try:
        lc_f = get_lc(f_expr)
        g = get_g()
        if g == 0:
            h3 = (lc_f != 0)
        else:
            h3 = (lc_f % g != 0)
    except Exception:
        h3 = False

    try:
        g = get_g()
        if g > 0 and sympy.isprime(g):
            p_mod = sympy.Poly(f_expr, x, domain=sympy.GF(g))
            h4 = p_mod.is_irreducible
        elif g == 0:
            p_mod = sympy.Poly(f_expr, x, domain=sympy.ZZ)
            h4 = p_mod.is_irreducible
        else:
            h4 = False
    except Exception:
        h4 = False

    try:
        deg_g = poly_degree(g_expr)
        deg_h = poly_degree(h_expr)
        
        diff = sympy.Poly(f_expr - (g_expr * h_expr), x)
        coeffs = diff.all_coeffs()
        is_eq = True
        for c in coeffs:
            if not c.is_integer:
                is_eq = False
                break
            val = int(c)
            if n > 0:
                if val % n != 0:
                    is_eq = False
                    break
            else:
                if val != 0:
                    is_eq = False
                    break
                    
        neg_q = (deg_g > 0) and (deg_h > 0) and is_eq
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of D",
    "H_2: f(x) is a non-constant polynomial over D",
    "H_3: The leading coefficient a_n is not an element of P",
    "H_4: The image of f(x) is irreducible over D/P",
    "¬Q: f(x) CAN be factored into two polynomials of positive degree over D"
]

N_HYP = 4
NEG_Q_INDEX = 4
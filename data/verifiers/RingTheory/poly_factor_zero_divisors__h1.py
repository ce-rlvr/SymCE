import sympy as sp
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices as matrices
import itertools

# Standard algebra objects
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
V4 = named_groups.AlternatingGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)

I2 = matrices.eye(2)
I3 = matrices.eye(3)
O2 = matrices.zeros(2, 2)
O3 = matrices.zeros(3, 3)

def is_multiple(g, f, n, x):
    f_poly = sp.Poly(f, x)
    g_poly = sp.Poly(g, x)
    
    if n > 0:
        g_coeffs = [c % n for c in g_poly.all_coeffs()] if not g_poly.is_zero else [0]
        f_coeffs = [c % n for c in f_poly.all_coeffs()] if not f_poly.is_zero else [0]
        g_poly = sp.Poly(g_coeffs, x)
        f_poly = sp.Poly(f_coeffs, x)
        
    if f_poly.is_zero:
        return g_poly.is_zero
    if g_poly.is_zero:
        return True
        
    df = f_poly.degree()
    dg = g_poly.degree()
    if dg < df:
        return False
    dq = dg - df
    
    if n == 0:
        _, r = sp.div(g_poly, f_poly)
        return r.is_zero
    else:
        if n**(dq + 1) > 100000:
            return False
        for coeffs in itertools.product(range(n), repeat=dq+1):
            q = sum(c * x**i for i, c in enumerate(coeffs))
            diff = sp.expand(g_poly.as_expr() - f_poly.as_expr() * q)
            diff_poly = sp.Poly(diff, x)
            if diff_poly.is_zero or all(c % n == 0 for c in diff_poly.coeffs()):
                return True
        return False

def is_zero_divisor(g, f, n, x):
    f_poly = sp.Poly(f, x)
    if n > 0:
        f_coeffs = [c % n for c in f_poly.all_coeffs()] if not f_poly.is_zero else [0]
        f_poly = sp.Poly(f_coeffs, x)
        
    df = f_poly.degree()
    if n == 0:
        gcd_fg = sp.gcd(f, g)
        gcd_poly = sp.Poly(gcd_fg, x)
        return gcd_poly.degree() > 0 or (gcd_poly.LC() not in [1, -1])
    else:
        search_deg = max(1, df + 1)
        if n**search_deg > 100000:
            return False
        for h_coeffs in itertools.product(range(n), repeat=search_deg):
            if all(c == 0 for c in h_coeffs):
                continue
            h = sum(c * x**i for i, c in enumerate(h_coeffs))
            if not is_multiple(h, f, n, x):
                if is_multiple(sp.expand(g * h), f, n, x):
                    return True
        return False

def conditions(witness):
    x = sp.Symbol('x')
    
    if isinstance(witness, tuple):
        if len(witness) == 3:
            f_expr, g_expr, n = witness
        elif len(witness) == 2:
            f_expr, g_expr = witness
            n = 0
            if hasattr(f_expr, 'domain') and hasattr(f_expr.domain, 'mod'):
                n = f_expr.domain.mod
        else:
            return [False, False, False]
    else:
        return [False, False, False]
        
    try:
        f = sp.expand(sp.sympify(f_expr))
        g = sp.expand(sp.sympify(g_expr))
    except Exception:
        return [False, False, False]
        
    # H1: f(x) is a non-zero polynomial
    try:
        if n == 0:
            h1 = not sp.Poly(f, x).is_zero
        else:
            f_poly = sp.Poly(f, x)
            h1 = not (f_poly.is_zero or all(c % n == 0 for c in f_poly.coeffs()))
    except Exception:
        h1 = False
        
    # H2: f(x) does not divide g(x)
    try:
        h2 = not is_multiple(g, f, n, x)
    except Exception:
        h2 = False
        
    # Conclusion: g(x) + <f(x)> is a zero divisor iff gcd(f(x), g(x)) != 1
    try:
        is_zd = is_zero_divisor(g, f, n, x)
        
        if n == 0:
            gcd_fg = sp.gcd(f, g)
            gcd_poly = sp.Poly(gcd_fg, x)
            gcd_is_one = gcd_poly.degree() == 0 and gcd_poly.LC() in [1, -1]
        else:
            if sp.isprime(n):
                gcd_fg = sp.gcd(f, g, domain=sp.GF(n))
                gcd_poly = sp.Poly(gcd_fg, x, domain=sp.GF(n))
                gcd_is_one = gcd_poly.degree() == 0
            else:
                gcd_fg = sp.gcd(f, g)
                gcd_poly = sp.Poly(gcd_fg, x)
                if gcd_poly.degree() == 0:
                    lc = gcd_poly.LC() % n
                    gcd_is_one = sp.gcd(lc, n) == 1
                else:
                    gcd_is_one = False
                
        gcd_not_one = not gcd_is_one
        
        conclusion = (is_zd == gcd_not_one)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a non-zero polynomial",
    "H_2: f(x) does not divide g(x)",
    "¬Q: g(x) + <f(x)> is a zero divisor iff gcd(f(x), g(x)) != 1 is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import Poly, Dummy, factor_list, RootOf, sqf_list, invert, expand
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_root_y(fac, sym, alpha, y, g_y):
    fac_poly = Poly(fac, sym)
    c = fac_poly.coeff_monomial(sym**1)
    d = fac_poly.coeff_monomial(sym**0)
    c_y = c.subs(alpha, y)
    d_y = d.subs(alpha, y)
    
    if c_y == 1:
        root_y = -d_y
        try:
            root_y = Poly(root_y, y, domain='QQ').rem(Poly(g_y, y, domain='QQ')).as_expr()
        except Exception:
            pass
        return root_y
        
    try:
        c_poly = Poly(c_y, y, domain='QQ')
        g_poly = Poly(g_y, y, domain='QQ')
        c_inv = invert(c_poly, g_poly).as_expr()
        root_y = expand(-d_y * c_inv)
        root_y = Poly(root_y, y, domain='QQ').rem(g_poly).as_expr()
        return root_y
    except Exception:
        return (-d_y / c_y)

def eval_poly_mod(P_expr, Q_expr, y, g_poly_y):
    P_poly = Poly(P_expr, y, domain='QQ')
    coeffs = P_poly.all_coeffs()
    res = Poly(0, y, domain='QQ')
    Q_poly = Poly(Q_expr, y, domain='QQ')
    
    for c in coeffs:
        res = res * Q_poly + Poly(c, y, domain='QQ')
        res = res.rem(g_poly_y)
        
    return res.as_expr()

def check_neg_Q(f_poly, g_poly, sym):
    y = Dummy('y')
    
    if not g_poly.is_irreducible:
        return False
        
    alpha = RootOf(g_poly.as_expr(), 0)
    g_y = g_poly.as_expr().subs(sym, y)
    g_poly_y = Poly(g_y, y, domain='QQ')
    
    try:
        f_facs = factor_list(f_poly.as_expr(), extension=alpha)[1]
    except Exception:
        return False
        
    P_y_list = []
    for fac, mult in f_facs:
        if Poly(fac, sym).degree() != 1:
            return False
        P_y = get_root_y(fac, sym, alpha, y, g_y)
        P_y_list.append(P_y)
        
    try:
        g_facs = factor_list(g_poly.as_expr(), extension=alpha)[1]
    except Exception:
        return False
        
    Q_y_list = []
    for fac, mult in g_facs:
        if Poly(fac, sym).degree() != 1:
            return False
        Q_y = get_root_y(fac, sym, alpha, y, g_y)
        Q_y_list.append(Q_y)
        
    kernel_size = 0
    
    for Q_y in Q_y_list:
        fixes_all = True
        for P_y in P_y_list:
            try:
                rem = eval_poly_mod(P_y, Q_y, y, g_poly_y)
                rem_orig = Poly(P_y, y, domain='QQ').rem(g_poly_y).as_expr()
                if expand(rem - rem_orig) != 0:
                    fixes_all = False
                    break
            except Exception:
                fixes_all = False
                break
        if fixes_all:
            kernel_size += 1
            
    return kernel_size > 1

def conditions(witness) -> list[bool]:
    try:
        f, g = witness
        if isinstance(f, list) and isinstance(g, list):
            sym = x
            f_poly = Poly.from_list(f, gens=sym, domain='QQ')
            g_poly = Poly.from_list(g, gens=sym, domain='QQ')
        else:
            if hasattr(f, 'free_symbols') and hasattr(g, 'free_symbols'):
                symbols = f.free_symbols | g.free_symbols
                if len(symbols) == 1:
                    sym = list(symbols)[0]
                elif len(symbols) == 0:
                    sym = x
                else:
                    return [False, False, False]
            else:
                sym = x
            f_poly = Poly(f, sym, domain='QQ')
            g_poly = Poly(g, sym, domain='QQ')
    except Exception:
        return [False, False, False]
        
    # H_1: K is a field (We are working over QQ, which is a field)
    h1_ok = True
    
    # H_2: f(x) is a separable polynomial of degree n
    try:
        sqf = sqf_list(f_poly)
        h2_ok = all(mult == 1 for fac, mult in sqf[1]) and f_poly.degree() > 0
    except Exception:
        h2_ok = False
        
    # ¬Q: The homomorphism from Gal(L/K) to S_n is not injective
    try:
        neg_q = check_neg_Q(f_poly, g_poly, sym)
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f(x) is a separable polynomial of degree n",
    "¬Q: The homomorphism from Gal(L/K) to S_n is not injective"
]

N_HYP = 2
NEG_Q_INDEX = 2
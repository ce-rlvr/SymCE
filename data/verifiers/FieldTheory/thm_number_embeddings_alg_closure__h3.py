import sympy
from sympy import Poly, Symbol, factor_list, QQ, sympify, RootOf
from sympy.abc import x

# Top-level setup
# K, L, E can be represented using QQ and polynomials in x.
# For example, witness = ('QQ', x**2 - 2, 2, 'QQ')

def get_var(expr, default_var):
    try:
        free = expr.free_symbols
        if len(free) == 1:
            return list(free)[0]
    except Exception:
        pass
    return default_var

def get_poly_expr(obj):
    try:
        if hasattr(obj, 'ext') and hasattr(obj.ext, 'minpoly'):
            return obj.ext.minpoly
    except Exception:
        pass
    return sympify(obj)

def get_degree(f, var):
    try:
        if hasattr(f, 'degree'):
            return f.degree()
        return Poly(f, var).degree()
    except Exception:
        return 0

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            K = witness.get('K')
            L = witness.get('L')
            n = witness.get('n')
            E = witness.get('E')
        else:
            K, L, n, E = witness
    except Exception:
        return [False, False, False]

    # H1: K is a field
    try:
        if K == 'QQ' or K == QQ:
            h1 = True
            domain_K = QQ
        elif hasattr(K, 'is_Field') and K.is_Field:
            h1 = True
            domain_K = K
        else:
            h1 = False
            domain_K = None
    except Exception:
        h1 = False
        domain_K = None

    # H2: L is a finite separable field extension of K of degree n
    try:
        if h1:
            L_expr = get_poly_expr(L)
            var_L = get_var(L_expr, x)
            poly_L = Poly(L_expr, var_L, domain=domain_K)
            is_irred = poly_L.is_irreducible
            n_int = int(n)
            deg_match = (poly_L.degree() == n_int)
            # In characteristic 0 (like QQ) or finite fields, irreducible implies separable.
            h2 = bool(is_irred and deg_match and n_int > 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: There are exactly n distinct field homomorphisms from L to E that fix K pointwise
    try:
        L_expr = get_poly_expr(L)
        var_L = get_var(L_expr, x)
        n_int = int(n)
        
        if E == 'QQ' or E == QQ or E == K:
            factors = factor_list(L_expr, var_L, domain=domain_K)[1]
            num_homs = sum(1 for f, m in factors if get_degree(f, var_L) == 1)
        elif E == 'QQ_bar':
            num_homs = n_int
        else:
            E_expr = get_poly_expr(E)
            r = RootOf(E_expr, 0)
            factors = factor_list(L_expr, var_L, extension=r)[1]
            num_homs = sum(1 for f, m in factors if get_degree(f, var_L) == 1)
        
        neg_q = bool(num_homs != n_int)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: L is a finite separable field extension of K of degree n",
    "¬Q: The number of distinct field homomorphisms from L to E fixing K is not exactly n"
]

N_HYP = 2
NEG_Q_INDEX = 2
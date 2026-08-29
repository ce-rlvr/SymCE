import sympy
from sympy import Symbol, Poly, RootOf, rem, expand
from sympy.abc import x, y, z

def get_roots_and_check_split(poly_expr, minpoly_K, a, x):
    try:
        if hasattr(a, 'is_Rational') and a.is_Rational:
            p = Poly(poly_expr, x, domain='QQ')
        else:
            p = Poly(poly_expr, x, extension=a)
        factors = p.factor_list()[1]
    except Exception:
        return False, []
    
    roots = []
    splits_completely = True
    for fac, mult in factors:
        if fac.degree() == 1:
            coeffs = fac.all_coeffs()
            c1 = coeffs[0]
            c0 = coeffs[1]
            root_val = -c0 / c1
            
            if hasattr(root_val, 'rep'):
                rep = root_val.rep
                if hasattr(rep, 'to_list'):
                    r_coeffs = rep.to_list()
                elif hasattr(rep, 'all_coeffs'):
                    r_coeffs = rep.all_coeffs()
                else:
                    r_coeffs = list(rep)
                root_poly_expr = Poly(r_coeffs, x).as_expr()
            elif hasattr(root_val, 'to_list'):
                r_coeffs = root_val.to_list()
                root_poly_expr = Poly(r_coeffs, x).as_expr()
            else:
                root_poly_expr = sympy.sympify(root_val)
                if not (hasattr(a, 'is_Rational') and a.is_Rational):
                    root_poly_expr = root_poly_expr.subs(a, x)
                
            root_poly_expr = expand(rem(root_poly_expr, minpoly_K, x))
            roots.extend([root_poly_expr] * mult)
        else:
            splits_completely = False
    return splits_completely, roots

def conditions(witness):
    try:
        minpoly_K, f = witness
        p_min = Poly(minpoly_K, x, domain='QQ')
        p_f = Poly(f, x, domain='QQ')
    except Exception:
        return [False, False, False]
        
    # H1: K/F is a Galois field extension.
    h1 = False
    automorphisms = []
    try:
        if p_min.is_irreducible:
            a = RootOf(minpoly_K, 0)
            splits_min, minpoly_roots = get_roots_and_check_split(minpoly_K, minpoly_K, a, x)
            if splits_min:
                h1 = True
                for r in minpoly_roots:
                    r_simp = expand(rem(r, minpoly_K, x))
                    if r_simp not in automorphisms:
                        automorphisms.append(r_simp)
    except Exception:
        h1 = False

    # H2: f has at least one root in K.
    h2 = False
    splits_f = False
    unique_roots_f = []
    try:
        if h1:
            splits_f, roots_f = get_roots_and_check_split(f, minpoly_K, a, x)
            for r in roots_f:
                r_simp = expand(rem(r, minpoly_K, x))
                if r_simp not in unique_roots_f:
                    unique_roots_f.append(r_simp)
            if len(unique_roots_f) > 0:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: f does not factor completely in K, or Gal(K/F) does not act transitively on its roots
    neg_q = False
    try:
        if h1:
            if not splits_f:
                neg_q = True
            else:
                if len(unique_roots_f) > 0:
                    r0 = unique_roots_f[0]
                    orbit = []
                    for sigma in automorphisms:
                        img = expand(r0.subs(x, sigma))
                        img = expand(rem(img, minpoly_K, x))
                        if img not in orbit:
                            orbit.append(img)
                    if len(orbit) < len(unique_roots_f):
                        neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K/F is a Galois field extension",
    "H_2: f has at least one root in K",
    "¬Q: f does not factor completely in K, or Gal(K/F) does not act transitively on its roots"
]

N_HYP = 2
NEG_Q_INDEX = 2
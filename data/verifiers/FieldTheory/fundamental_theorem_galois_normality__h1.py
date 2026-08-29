import sympy
from sympy import Symbol, Poly, CRootOf, factor, invert, resultant, factor_list

x = Symbol('x')
y = Symbol('y')

def conditions(witness):
    """
    Witness should be a tuple of two polynomials (f, g) in x with rational coefficients.
    - f is the minimal polynomial of a primitive element 'a' of K over Q. (So K = Q(a))
    - g is a polynomial such that E = Q(g(a)).
    This automatically satisfies F \subseteq E \subseteq K with F = Q.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        f, g = witness
        
        # H1: f is an irreducible polynomial over Q, g is a polynomial
        try:
            poly_f = Poly(f, x, domain='QQ')
            poly_g = Poly(g, x, domain='QQ')
            if poly_f.degree() < 1:
                h1 = False
            else:
                h1 = bool(poly_f.is_irreducible)
        except Exception:
            h1 = False
            
        # Evaluate conclusion
        try:
            if not h1:
                neg_q = False
            else:
                a = CRootOf(f, 0)
                
                # Get Aut(K/Q)
                aut_K_Q = []
                factored_f = factor(f, extension=a)
                factors_f = factored_f.args if factored_f.is_Mul else [factored_f]
                for fac in factors_f:
                    fac_base = fac.base if fac.is_Pow else fac
                    p_poly = Poly(fac_base, x)
                    if p_poly.degree() == 1:
                        c = p_poly.coeff_monomial(x)
                        d = p_poly.coeff_monomial(1)
                        c_x = c.subs(a, x)
                        d_x = d.subs(a, x)
                        try:
                            c_inv = invert(c_x, f)
                        except Exception:
                            c_inv = 1 / c_x
                        p_x = Poly(-d_x * c_inv, x).rem(poly_f).as_expr()
                        aut_K_Q.append(p_x)
                        
                # Get Aut(K/E)
                aut_K_E = []
                for p in aut_K_Q:
                    g_p = poly_g.as_expr().subs(x, p)
                    rem = Poly(g_p - poly_g.as_expr(), x).rem(poly_f)
                    if rem.is_zero:
                        aut_K_E.append(p)
                        
                # Check if Aut(K/E) is normal in Aut(K/Q)
                def compose(p1, p2):
                    return Poly(p1.subs(x, p2), x).rem(poly_f).as_expr()
                    
                is_normal = True
                for g_elem in aut_K_Q:
                    gH = []
                    Hg = []
                    for h_elem in aut_K_E:
                        gH.append(compose(g_elem, h_elem))
                        Hg.append(compose(h_elem, g_elem))
                    
                    for p1 in gH:
                        found = False
                        for p2 in Hg:
                            if Poly(p1, x) == Poly(p2, x):
                                found = True
                                break
                        if not found:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                        
                # Check if E/Q is normal
                h_res = resultant(f, y - g, x)
                factors_h = factor_list(h_res)[1]
                minpoly_b = None
                for fac, mult in factors_h:
                    if fac.has(y) and Poly(fac, y).degree() > 0:
                        lc = Poly(fac, y).LC()
                        minpoly_b = (fac / lc).expand()
                        break
                        
                if minpoly_b is None:
                    e_is_normal = False
                else:
                    deg_b = Poly(minpoly_b, y).degree()
                    if deg_b <= 1:
                        e_is_normal = True
                    else:
                        b_root = CRootOf(minpoly_b, 0)
                        factored_b = factor(minpoly_b, extension=b_root)
                        factors_b = factored_b.args if factored_b.is_Mul else [factored_b]
                        linear_count = 0
                        for fac in factors_b:
                            fac_base = fac.base if fac.is_Pow else fac
                            if Poly(fac_base, y).degree() == 1:
                                linear_count += fac.exp if fac.is_Pow else 1
                        e_is_normal = (linear_count == deg_b)
                        
                # The conclusion states: E/F is normal iff Gal(K/E) is normal in Gal(K/F)
                conclusion = (e_is_normal == is_normal)
                neg_q = not conclusion
                
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: E is an intermediate field such that F \\subseteq E \\subseteq K",
    "¬Q: E/F is normal iff Gal(K/E) is normal in Gal(K/F) is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1
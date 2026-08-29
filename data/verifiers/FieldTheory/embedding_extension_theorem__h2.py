import sympy
from sympy import Poly, factor_list, RootOf, minpoly, simplify
from sympy.abc import x

# Top-level setup
# The witness should be a tuple of polynomials in x with rational coefficients.
# Format 1: (E_poly, L_poly) 
#           Implicitly assumes F = Q, so F_poly = x, and embeddings are trivial (0).
# Format 2: (F_poly, E_poly, L_poly, emb_F_E, emb_F_L)
#           F_poly, E_poly, L_poly are minimal polynomials defining the fields F, E, L.
#           emb_F_E is a polynomial representing the image of F's generator in E.
#           emb_F_L is a polynomial representing the image of F's generator in L (\sigma).

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 2:
            E_poly, L_poly = witness
            F_poly = x
            emb_F_E = 0
            emb_F_L = 0
        elif len(witness) == 5:
            F_poly, E_poly, L_poly, emb_F_E, emb_F_L = witness
        else:
            return [False, False, False]
            
        def check_embedding(poly_domain, poly_codomain, emb):
            p_dom = Poly(poly_domain, x, domain='QQ')
            p_codom = Poly(poly_codomain, x, domain='QQ')
            p_emb = Poly(emb, x, domain='QQ')
            res = Poly(0, x, domain='QQ')
            for c in p_dom.all_coeffs():
                res = res * p_emb + Poly(c, x, domain='QQ')
                res = res.rem(p_codom)
            return res.is_zero

        # H1: E is an algebraic field extension of F
        h1 = False
        if Poly(F_poly, x, domain='QQ').is_irreducible and Poly(E_poly, x, domain='QQ').is_irreducible:
            if check_embedding(F_poly, E_poly, emb_F_E):
                h1 = True
                
        # H2: sigma: F -> L is a field embedding
        h2 = False
        if Poly(L_poly, x, domain='QQ').is_irreducible:
            if check_embedding(F_poly, L_poly, emb_F_L):
                h2 = True
                
        # Negated Conclusion: NO extension exists
        # We check if there is any root of E_poly in L that restricts to sigma on F.
        neg_q = True
        if h1 and h2:
            theta = RootOf(L_poly, 0)
            factors = factor_list(E_poly, extension=theta)[1]
            
            p_emb_F_E = Poly(emb_F_E, x, domain='QQ')
            p_emb_F_L = Poly(emb_F_L, x, domain='QQ')
            
            for fac, mult in factors:
                fac_poly = Poly(fac, x)
                if fac_poly.degree() == 1:
                    c1 = fac_poly.coeff_monomial(x**1)
                    c0 = fac_poly.coeff_monomial(x**0)
                    root_expr = -c0 / c1
                    
                    val1 = 0
                    for c in p_emb_F_E.all_coeffs():
                        val1 = val1 * root_expr + c
                        
                    val2 = 0
                    for c in p_emb_F_L.all_coeffs():
                        val2 = val2 * theta + c
                        
                    diff = val1 - val2
                    if diff == 0 or simplify(diff) == 0:
                        neg_q = False
                        break
                    try:
                        if minpoly(diff, x) == x:
                            neg_q = False
                            break
                    except Exception:
                        pass
                        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: E is an algebraic field extension of F",
    "H_2: sigma: F -> L is a field embedding",
    "¬Q: There does not exist a field embedding E -> L extending sigma"
]

N_HYP = 2
NEG_Q_INDEX = 2
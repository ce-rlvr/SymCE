import sympy
from sympy import Poly, factor_list, RootOf, expand
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        # The witness should be a tuple (f, g) of two polynomials in x.
        # K is the field of rational numbers QQ.
        # f is the polynomial to test.
        # g is the minimal polynomial of a primitive element of L, so L = QQ[x]/(g(x)).
        f, g = witness
        f_poly = Poly(f, x, domain='QQ')
        g_poly = Poly(g, x, domain='QQ')
        
        # H1: f is irreducible over K (QQ)
        h1 = f_poly.is_irreducible
        
        # H2 requires L to be a field, so g must be irreducible over QQ
        g_irred = g_poly.is_irreducible
        if not g_irred:
            return [False, False, False]
            
        alpha = RootOf(g_poly.as_expr(), 0)
        
        # Factor f over L = QQ(alpha)
        fact_f = factor_list(f_poly.as_expr(), extension=alpha)
        
        # Find all roots of f in L (corresponding to linear factors)
        roots_f = []
        for fac, mult in fact_f[1]:
            p = Poly(fac, x)
            if p.degree() == 1:
                coeffs = p.all_coeffs()
                # Since factors are monic, coeffs[0] is 1
                gamma_alpha = -coeffs[1] / coeffs[0]
                gamma_x = gamma_alpha.subs(alpha, x)
                roots_f.append(gamma_x)
                
        # H2: f has at least one root in L
        h2 = len(roots_f) >= 1
        
        # Conclusion: f splits completely in L AND Gal(L/K) acts transitively
        deg_f = f_poly.degree()
        splits_completely = (len(roots_f) == deg_f)
        
        if not splits_completely:
            transitive = False
        else:
            # Find automorphisms of L/K by factoring g over L
            fact_g = factor_list(g_poly.as_expr(), extension=alpha)
            automorphisms = []
            for fac, mult in fact_g[1]:
                p = Poly(fac, x)
                if p.degree() == 1:
                    coeffs = p.all_coeffs()
                    beta_alpha = -coeffs[1] / coeffs[0]
                    beta_x = beta_alpha.subs(alpha, x)
                    automorphisms.append(beta_x)
            
            # Check transitivity of the Galois group action on the roots of f
            orbit = set()
            gamma_x = roots_f[0]
            for beta_x in automorphisms:
                composed = gamma_x.subs(x, beta_x)
                rem = Poly(composed, x).rem(g_poly)
                orbit.add(expand(rem.as_expr()))
                
            transitive = (len(orbit) == deg_f)
            
        neg_q = not (splits_completely and transitive)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f(x) is an irreducible polynomial over K",
    "H_2: f(x) has at least one root in L",
    "¬Q: f(x) does not split completely in L, or Gal(L/K) does not act transitively on its roots"
]

N_HYP = 2
NEG_Q_INDEX = 2
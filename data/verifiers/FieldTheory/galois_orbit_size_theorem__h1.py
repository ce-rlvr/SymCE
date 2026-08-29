import sympy as sp
from sympy import Poly, Symbol, Matrix, real_roots

x = Symbol('x')

CONDITION_LABELS = [
    "H_1: alpha is an element of E",
    "¬Q: The cardinality of the orbit of alpha under the action of G is not equal to the degree of the minimal polynomial of alpha over F"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, dict):
            return [False, False]
            
        p_min_expr = witness.get('minpoly')
        alpha_expr = witness.get('alpha')
        G_exprs = witness.get('G')
        
        if p_min_expr is None or alpha_expr is None or G_exprs is None:
            return [False, False]
            
        p_min = Poly(p_min_expr, x, domain='QQ')
        alpha = Poly(alpha_expr, x, domain='QQ')
        G = [Poly(g, x, domain='QQ') for g in G_exprs]
        
        # Verify E is a valid field extension over Q
        is_field = p_min.is_irreducible
        
        # Verify G is a valid group of automorphisms of E/Q
        is_aut = True
        for g in G:
            p_g_expr = p_min.as_expr().subs(x, g.as_expr())
            p_g = Poly(p_g_expr, x, domain='QQ')
            if (p_g % p_min) != 0:
                is_aut = False
                break
                
        for g1 in G:
            for g2 in G:
                comp_expr = g1.as_expr().subs(x, g2.as_expr())
                comp = Poly(comp_expr, x, domain='QQ') % p_min
                if not any(comp == g for g in G):
                    is_aut = False
                    break
                    
        # To ensure the witness is a genuine counterexample to the dropped Galois hypothesis,
        # we enforce that E/Q is not Galois. A simple and rigorous way is to require a polynomial
        # with exactly 1 real root and degree > 1 (e.g., x^3 - 2).
        # In this case, the full automorphism group must have size 1.
        rr = real_roots(p_min.as_expr())
        is_not_galois = (len(rr) == 1 and p_min.degree() > 1)
        is_full_aut = (len(G) == 1)
        
        h1 = bool(is_field and is_aut and is_not_galois and is_full_aut)
        
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, dict):
            return [h1, False]
            
        p_min_expr = witness.get('minpoly')
        alpha_expr = witness.get('alpha')
        G_exprs = witness.get('G')
        
        if p_min_expr is None or alpha_expr is None or G_exprs is None:
            return [h1, False]
            
        p_min = Poly(p_min_expr, x, domain='QQ')
        alpha = Poly(alpha_expr, x, domain='QQ')
        G = [Poly(g, x, domain='QQ') for g in G_exprs]
        
        deg_E = p_min.degree()
        
        # Compute the cardinality of the orbit of alpha under G
        orbit = set()
        for g in G:
            img_expr = alpha.as_expr().subs(x, g.as_expr())
            img = Poly(img_expr, x, domain='QQ') % p_min
            coeffs = img.all_coeffs()
            # Pad with leading zeros to ensure unique tuple representation
            coeffs = tuple([0]*(deg_E - len(coeffs)) + coeffs)
            orbit.add(coeffs)
        orbit_size = len(orbit)
        
        # Compute the degree of the minimal polynomial of alpha over Q
        vecs = []
        alpha_pow = Poly(1, x, domain='QQ')
        deg_alpha = 0
        for i in range(deg_E + 1):
            coeffs = alpha_pow.all_coeffs()
            coeffs = [0]*(deg_E - len(coeffs)) + coeffs
            vecs.append(coeffs)
            
            M = Matrix(vecs).T
            if M.rank() < len(vecs):
                deg_alpha = i
                break
                
            alpha_pow = Poly((alpha_pow * alpha) % p_min, x, domain='QQ')
            
        neg_q = bool(orbit_size != deg_alpha)
        
    except Exception:
        neg_q = False

    return [h1, neg_q]
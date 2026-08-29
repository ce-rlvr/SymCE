import sympy
from sympy import Poly, Symbol, Abs, im
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be either:
      - A single SymPy expression `poly_L` in `x` (implicitly setting K=QQ, E=QQ).
      - A tuple `(poly_L, poly_E, h)` of SymPy expressions in `x`, where:
          L = QQ[x]/(poly_L)
          E = QQ[x]/(poly_E)
          h is the embedding of E into L, i.e., poly_E(h(x)) = 0 mod poly_L(x).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            poly_L, poly_E, h = witness
        else:
            poly_L = witness
            poly_E = x
            h = 0
            
        poly_L_expr = Poly(poly_L, x, domain='QQ')
        poly_E_expr = Poly(poly_E, x, domain='QQ')
        h_expr = Poly(h, x, domain='QQ')
    except Exception:
        return [False, False]
        
    # Hypothesis 1: E is an intermediate field such that K \subseteq E \subseteq L
    # We verify this by checking that poly_L and poly_E are irreducible over QQ,
    # and that h defines a valid embedding of E into L.
    try:
        h1_ok = False
        if poly_L_expr.is_irreducible and poly_E_expr.is_irreducible:
            comp_expr = poly_E_expr.as_expr().subs(x, h_expr.as_expr())
            comp = Poly(comp_expr, x, domain='QQ')
            _, rem = comp.div(poly_L_expr)
            if rem.is_zero:
                h1_ok = True
    except Exception:
        h1_ok = False
        
    # Conclusion: L/E is a normal extension
    # We want this to FAIL, so we check if L/E is NOT normal.
    # If L has a real embedding, then any normal extension over E must have all 
    # conjugate roots of the generator be real. If there are complex conjugates, 
    # they cannot lie in the real field L, hence the extension is not normal.
    try:
        neg_q = False
        if poly_E_expr.degree() > 0:
            d = poly_L_expr.degree() // poly_E_expr.degree()
            roots = poly_L_expr.nroots(n=50)
            
            for beta in roots:
                # Find a real root to define a real embedding of L
                if Abs(im(beta)) > 1e-25:
                    continue
                    
                val = h_expr.as_expr().subs(x, beta).evalf(50)
                
                # Find all roots of poly_L that map to the same value under h
                # These correspond to the roots of the minimal polynomial of beta over E
                matching_roots = []
                for r in roots:
                    r_val = h_expr.as_expr().subs(x, r).evalf(50)
                    if Abs(r_val - val) < 1e-20:
                        matching_roots.append(r)
                        
                # If the minimal polynomial over E does not split completely in L,
                # then L/E is not normal. Since L is real, any complex root among
                # the matching roots proves it doesn't split in L.
                if len(matching_roots) == d:
                    real_matching = [r for r in matching_roots if Abs(im(r)) < 1e-25]
                    if len(real_matching) < d:
                        neg_q = True
                        break
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: E is an intermediate field such that K \\subseteq E \\subseteq L",
    "¬Q: The extension L/E is not a normal extension"
]

N_HYP = 1
NEG_Q_INDEX = 1
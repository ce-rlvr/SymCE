import sympy
from sympy.abc import x

# Top-level setup
# The witness is expected to be a tuple: (min_poly_expr, image_poly_expr)
# representing a finite field extension E = Q[x]/(min_poly_expr) over F = Q,
# and an F-automorphism σ defined by σ(x) = image_poly_expr.

def conditions(witness):
    try:
        # Unpack the witness
        if len(witness) != 2:
            return [False, False]
        min_poly_expr, image_poly_expr = witness
        
        # Convert to sympy expressions
        min_poly_expr = sympy.sympify(min_poly_expr)
        image_poly_expr = sympy.sympify(image_poly_expr)
        
        # Create polynomials over the rationals
        min_poly = sympy.Poly(min_poly_expr, x, domain='QQ')
        image_poly = sympy.Poly(image_poly_expr, x, domain='QQ')
        
        # The minimal polynomial must define a valid field extension of degree >= 1
        if min_poly.degree() < 1:
            return [False, False]
            
        # Check if E is a field (min_poly is irreducible over QQ)
        is_irred = min_poly.is_irreducible
        
        # Check if σ is a valid F-homomorphism from E to E
        # This requires that substituting image_poly into min_poly yields 0 mod min_poly
        comp_expr = min_poly.as_expr().subs(x, image_poly.as_expr())
        comp_poly = sympy.Poly(comp_expr, x, domain='QQ')
        _, rem = comp_poly.div(min_poly)
        
        is_hom = rem.is_zero
        
        # Since E is a finite field extension, any non-zero F-endomorphism is an F-automorphism.
        h1_ok = bool(is_irred and is_hom)
        
        # Check if σ is the identity automorphism
        # This requires image_poly(x) == x mod min_poly
        id_expr = image_poly.as_expr() - x
        id_poly = sympy.Poly(id_expr, x, domain='QQ')
        _, rem_id = id_poly.div(min_poly)
        
        # Negated conclusion: σ is NOT the identity
        neg_q_ok = not rem_id.is_zero
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: σ is an F-automorphism of E",
    "¬Q: σ is not the identity automorphism on E"
]

N_HYP = 1
NEG_Q_INDEX = 1
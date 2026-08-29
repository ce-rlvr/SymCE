import sympy as sp
import math

x = sp.Symbol('x')

CONDITION_LABELS = [
    "H_1: E/K is an arbitrary field extension",
    "H_2: L and E are subfields of a common larger field",
    "¬Q: The compositum LE is not a Galois extension of E, or the restriction map is not an isomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        poly_L, poly_E = witness
        
        # Ensure the polynomials are expressions in x
        if hasattr(poly_L, 'free_symbols') and poly_L.free_symbols:
            var = list(poly_L.free_symbols)[0]
            poly_L = poly_L.subs(var, x)
        if hasattr(poly_E, 'free_symbols') and poly_E.free_symbols:
            var = list(poly_E.free_symbols)[0]
            poly_E = poly_E.subs(var, x)
            
        poly_L = sp.Poly(poly_L, x, domain='QQ')
        poly_E = sp.Poly(poly_E, x, domain='QQ')
        
        if not poly_L.is_irreducible or not poly_E.is_irreducible:
            return [False, False, False]
            
        deg_L = poly_L.degree()
        deg_E = poly_E.degree()
        
        h1 = True
        h2 = True
        
        # To reliably compute the intersection L \cap E, we restrict our evaluation
        # to cases where L \cap E = Q, which is guaranteed if gcd(deg_L, deg_E) == 1 or deg_E == 1.
        if math.gcd(deg_L, deg_E) != 1 and deg_E != 1:
            return [h1, h2, False]
            
        # Compute the number of Q-automorphisms of L (size of Gal(L / L \cap E) since L \cap E = Q)
        if deg_L == 1:
            alpha = sp.solve(poly_L.as_expr(), x)[0]
            size_Gal_L = 1
        else:
            alpha = sp.CRootOf(poly_L, 0)
            factors_L = sp.factor_list(poly_L, extension=alpha)[1]
            size_Gal_L = sum(1 for f, k in factors_L if f.degree() == 1)
            
        if deg_E == 1:
            beta = sp.solve(poly_E.as_expr(), x)[0]
        else:
            beta = sp.CRootOf(poly_E, 0)
            
        # Compute the primitive element for the compositum LE
        poly_LE, coeffs = sp.primitive_element([alpha, beta], x, ex=True)
        c1_expr, c2_expr = coeffs
        
        deg_LE = poly_LE.degree()
        deg_LE_E = deg_LE // deg_E
        
        # Compute the number of E-automorphisms of LE (size of Gal(LE/E))
        if deg_LE == 1:
            size_Gal_LE_E = 1
        else:
            gamma = sp.CRootOf(poly_LE, 0)
            factors_LE = sp.factor_list(poly_LE, extension=gamma)[1]
            
            y = sp.Symbol('y')
            poly_LE_y = poly_LE.as_expr().subs(x, y)
            c2_gamma_y = c2_expr.subs(x, y)
            
            size_Gal_LE_E = 0
            for f, k in factors_LE:
                if f.degree() == 1:
                    f_expr = f.as_expr()
                    A = f_expr.diff(x)
                    B = f_expr.subs(x, 0)
                    root_expr = sp.cancel(-B / A)
                    root_y = root_expr.subs(gamma, y)
                    
                    # Check if this Q-automorphism fixes E (i.e., fixes beta)
                    c2_val_y = c2_expr.subs(x, root_y)
                    diff_y = sp.expand(c2_val_y - c2_gamma_y)
                    rem = sp.rem(diff_y, poly_LE_y, y)
                    if rem == 0:
                        size_Gal_LE_E += 1
                        
        # The conclusion holds if LE/E is Galois AND the restriction map is an isomorphism
        is_Galois = (size_Gal_LE_E == deg_LE_E)
        is_iso = (size_Gal_LE_E == size_Gal_L)
        
        Q = is_Galois and is_iso
        neg_Q = not Q
        
        return [h1, h2, neg_Q]
    except Exception:
        return [False, False, False]
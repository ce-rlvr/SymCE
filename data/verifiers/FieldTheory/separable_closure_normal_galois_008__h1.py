import sympy
from sympy import Symbol, Poly, RootOf, factor_list

# Top-level setup
x = Symbol('x')

CONDITION_LABELS = [
    "H_1: E is the subfield of L consisting of all elements that are separable over K",
    "¬Q: E is not a Galois extension of K"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # The witness can be a single polynomial (defining L and E implicitly as the same field over Q),
        # or a tuple/list like (L_poly, E_poly) or (K, L, E).
        if isinstance(witness, (tuple, list)):
            if len(witness) >= 2:
                L_poly = witness[-2]
                E_poly = witness[-1]
            else:
                L_poly = witness[0]
                E_poly = witness[0]
        else:
            L_poly = witness
            E_poly = witness
            
        def extract_expr(poly_obj):
            # Handle SymPy AlgebraicField objects
            if hasattr(poly_obj, 'ext') and hasattr(poly_obj.ext, 'minpoly'):
                expr = poly_obj.ext.minpoly.as_expr()
            else:
                expr = sympy.sympify(poly_obj)
                
            # Handle equations like Eq(x**3 - 2, 0)
            if isinstance(expr, sympy.Eq):
                expr = expr.lhs - expr.rhs
                
            # Normalize variable to 'x' or compute minpoly for algebraic numbers
            if expr.free_symbols:
                var = list(expr.free_symbols)[0]
                expr = expr.subs(var, x)
            elif expr.is_number:
                expr = sympy.minpoly(expr, x)
                
            return expr

        L_expr = extract_expr(L_poly)
        E_expr = extract_expr(E_poly)
            
        L_p = Poly(L_expr, x, domain='QQ')
        E_p = Poly(E_expr, x, domain='QQ')
        
        h1 = False
        # Over Q, the separable closure of Q in L is L itself.
        # Thus, E must be equal to L. We check if they define the same number field.
        if L_p.is_irreducible and E_p.is_irreducible and L_p.degree() == E_p.degree():
            if L_p.monic() == E_p.monic():
                h1 = True
            else:
                # Check if E_p has a root in Q(alpha) where alpha is a root of L_p
                alpha_L = RootOf(L_p.expr, 0)
                factors_E_in_L = factor_list(E_p.expr, extension=alpha_L)
                for fac, mult in factors_E_in_L[1]:
                    if Poly(fac, x).degree() == 1:
                        h1 = True
                        break
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # neg_Q: E is NOT a Galois extension of K
            # E is Galois over Q iff its minimal polynomial splits completely in its own field.
            alpha_E = RootOf(E_p.expr, 0)
            factors_E = factor_list(E_p.expr, extension=alpha_E)
            
            is_galois = True
            for fac, mult in factors_E[1]:
                if Poly(fac, x).degree() > 1:
                    is_galois = False
                    break
            
            neg_q = not is_galois
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]
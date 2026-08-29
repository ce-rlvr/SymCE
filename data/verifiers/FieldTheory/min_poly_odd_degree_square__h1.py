import sympy
from sympy import Poly, Symbol, Dummy
from sympy.abc import x, y, z, t

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    "Generation of a Simple Extension by a Square for Odd Degree Minimal Polynomials"
    """
    h1, h2, h3, neg_q = False, False, False, False
    try:
        # Parse the witness into a minimal polynomial p over a field F
        if isinstance(witness, list):
            x_var = sympy.Symbol('x')
            p = sympy.Poly(witness, x_var)
        elif hasattr(witness, 'free_symbols') and len(witness.free_symbols) == 0:
            try:
                x_var = sympy.Symbol('x')
                p_expr = sympy.minpoly(witness, x_var)
                p = sympy.Poly(p_expr, x_var)
            except Exception:
                p = sympy.Poly(witness)
                if len(p.gens) != 1:
                    return [False, False, False, False]
                x_var = p.gens[0]
        else:
            p = sympy.Poly(witness)
            if len(p.gens) != 1:
                return [False, False, False, False]
            x_var = p.gens[0]
            
        # H_1: K is a field extension of F. 
        # This is true if the polynomial defining the extension is irreducible.
        h1 = bool(p.is_irreducible)
        
        # H_2: alpha in K is an algebraic element over F.
        # Since it is defined by a polynomial, it is algebraic.
        h2 = True
        
        # H_3: The degree of the minimal polynomial of alpha over F is an odd integer.
        h3 = bool(p.degree() % 2 == 1)
        
        # Evaluate Conclusion: F(alpha) == F(alpha^2) and degrees of minimal polynomials are equal.
        # We find the minimal polynomial of alpha^2 by computing the resultant of p(y) and x - y^2.
        y_dummy = sympy.Dummy('y')
        p_expr = p.as_expr()
        p_y_expr = p_expr.subs(x_var, y_dummy)
        
        # The resultant eliminates y_dummy and gives a polynomial in x_var that has alpha^2 as a root.
        res_expr = sympy.resultant(p_y_expr, x_var - y_dummy**2, y_dummy)
        res_poly = sympy.Poly(res_expr, x_var, domain=p.domain)
        
        # Factor the resultant to find the irreducible minimal polynomial of alpha^2
        factors = res_poly.factor_list()
        
        if not factors[1]:
            q = False
        else:
            # factors[1] contains tuples of (irreducible_factor, multiplicity)
            min_poly_alpha2 = factors[1][0][0]
            deg_equal = min_poly_alpha2.degree() == p.degree()
            # If the degrees are equal, then [F(alpha^2):F] = [F(alpha):F], which implies F(alpha) = F(alpha^2)
            q = deg_equal
            
        neg_q = not q
        
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field extension of F",
    "H_2: alpha in K is an algebraic element over F",
    "H_3: The degree of the minimal polynomial of alpha over F is an odd integer",
    "¬Q: F(alpha) != F(alpha^2) or the minimal polynomial of alpha^2 over F has a different degree"
]

N_HYP = 3
NEG_Q_INDEX = 3
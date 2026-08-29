import sympy
from sympy import Poly, cyclotomic_poly, RootOf
from sympy.abc import x

# Top-level setup
# We use x from sympy.abc for polynomial definitions.
x = sympy.abc.x

def conditions(witness):
    """
    witness is a tuple: (L_poly, zeta_poly, n)
    L_poly: minimal polynomial of a primitive element of L over Q.
    zeta_poly: minimal polynomial of zeta over Q.
    n: integer n for the n-th roots of unity.
    """
    try:
        if len(witness) != 3:
            return [False, False]
            
        L_poly_expr, zeta_poly_expr, n = witness
        
        L_poly_expr = sympy.sympify(L_poly_expr)
        zeta_poly_expr = sympy.sympify(zeta_poly_expr)
        
        L_poly = Poly(L_poly_expr, x, domain='QQ')
        zeta_poly = Poly(zeta_poly_expr, x, domain='QQ')
        n = int(n)
        
        if n < 1:
            return [False, False]
            
        if not L_poly.is_irreducible:
            return [False, False]
            
        if not zeta_poly.is_irreducible:
            return [False, False]
            
        # H1: L/K is a normal extension (we fix K = Q)
        deg = L_poly.degree()
        if deg <= 2:
            h1 = True
        elif deg <= 4:
            root = RootOf(L_poly.as_expr(), 0)
            factors = L_poly.factor_list(extension=root)[1]
            h1 = all(f[0].degree() == 1 for f in factors)
        else:
            h1 = False
            
        # Conclusion: All conjugates of zeta over K are primitive n-th roots of unity,
        # and they are contained in L.
        
        # 1. Are all conjugates primitive n-th roots of unity?
        # Over Q, this is true iff zeta_poly is exactly the n-th cyclotomic polynomial.
        cyclo = Poly(cyclotomic_poly(n, x), x, domain='QQ')
        is_primitive = (zeta_poly.monic() == cyclo)
        
        # 2. Are they contained in L?
        # This is true iff zeta_poly splits completely in L.
        if L_poly.degree() == 1:
            is_contained = (zeta_poly.degree() == 1)
        else:
            if zeta_poly.degree() > 10:
                is_contained = False
            else:
                root = RootOf(L_poly.as_expr(), 0)
                factors = zeta_poly.factor_list(extension=root)[1]
                is_contained = all(f[0].degree() == 1 for f in factors)
                
        q = is_primitive and is_contained
        neg_q = not q
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: L/K is a normal extension",
    "¬Q: Conjugates of zeta over K are not all primitive n-th roots of unity, or not all contained in L"
]

N_HYP = 1
NEG_Q_INDEX = 1
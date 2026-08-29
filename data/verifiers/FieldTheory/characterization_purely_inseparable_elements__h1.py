import sympy as sp
from sympy import Symbol, Poly, GF, QQ, ZZ
from sympy.abc import x, y, z, t

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    
    The witness represents an algebraic field extension E/K.
    It can be provided as a tuple (poly_expr, p) where poly_expr is the minimal 
    polynomial of a primitive element of E/K, and p is the characteristic of K.
    If provided as just poly_expr, characteristic p=0 is assumed.
    """
    try:
        if isinstance(witness, tuple):
            poly_expr, p = witness
        else:
            poly_expr = witness
            p = 0
            
        poly_expr = sp.sympify(poly_expr)
            
        if isinstance(poly_expr, Poly):
            poly_expr = poly_expr.as_expr()
            
        symbols = poly_expr.free_symbols
        if len(symbols) != 1:
            return [False, False]
        var = list(symbols)[0]
        
        if p == 0:
            f = Poly(poly_expr, var, domain=QQ)
            # H_1: E/K is an algebraic field extension (f is irreducible over K)
            h1 = f.is_irreducible and f.degree() >= 1
            
            # LHS: E/K is purely inseparable.
            # In characteristic 0, all extensions are separable, so purely inseparable implies E = K (degree 1).
            lhs = (f.degree() == 1)
            
            # RHS: for every alpha in E, exists n >= 0 such that alpha^{p^n} in K.
            # For p=0, choosing n=1 gives p^1 = 0, so alpha^0 = 1 in K.
            # This is trivially true for all elements in any extension.
            rhs = True
            
        else:
            f = Poly(poly_expr, var, domain=GF(p))
            # H_1: E/K is an algebraic field extension
            h1 = f.is_irreducible and f.degree() >= 1
            
            # In a finite field, all extensions are separable.
            # So purely inseparable implies E = K (degree 1).
            lhs = (f.degree() == 1)
            
            # RHS: alpha^{p^n} in K. For finite fields, this implies alpha in K.
            rhs = (f.degree() == 1)
            
        # The conclusion is the equivalence LHS <-> RHS.
        # We want the negated conclusion, so we check if the equivalence fails.
        neg_q = (lhs != rhs)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: E/K is an algebraic field extension",
    "¬Q: The equivalence (purely inseparable iff exists n>=0 such that alpha^{p^n} in K) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1
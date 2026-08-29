import sympy as sp

# Top-level setup
x, y, z = sp.symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the conjecture.
    The witness is expected to be an irreducible polynomial over QQ,
    representing the field extension K = QQ[x]/(witness).
    """
    try:
        expr = sp.sympify(witness)
        if isinstance(expr, sp.Equality):
            expr = expr.lhs - expr.rhs
            
        free_symbols = expr.free_symbols
        if len(free_symbols) != 1:
            return [False, False, False]
        var = list(free_symbols)[0]
        
        poly = sp.Poly(expr, var, domain='QQ')
    except Exception:
        return [False, False, False]
        
    # H_1: K is a field extension of F (witness is an irreducible polynomial over QQ)
    try:
        h1 = bool(poly.degree() >= 1 and poly.is_irreducible)
    except Exception:
        h1 = False
        
    # H_2: Aut(K/F) contains only the identity automorphism
    # This is true if the polynomial has exactly 1 root in the extension field K.
    try:
        if poly.degree() == 1:
            h2 = True
        else:
            # Let r be a root of the polynomial, so K = QQ(r)
            r = sp.RootOf(poly, 0)
            dummy = sp.Symbol('__dummy__')
            expr_dummy = expr.subs(var, dummy)
            
            # Factor the polynomial over the extension field QQ(r)
            factors = sp.factor_list(expr_dummy, extension=r)[1]
            
            # Count the number of linear factors (which correspond to roots in K)
            linear_factors = 0
            for fac, mult in factors:
                if sp.degree(fac, dummy) == 1:
                    linear_factors += 1
            h2 = bool(linear_factors == 1)
    except Exception:
        h2 = False
        
    # ¬Q: K is NOT a purely inseparable extension of F
    # Over a field of characteristic 0 (like QQ), an extension is purely 
    # inseparable if and only if it is the trivial extension (degree 1).
    try:
        neg_q = bool(poly.degree() > 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field extension of F (witness is an irreducible polynomial over QQ)",
    "H_2: Aut(K/F) contains only the identity automorphism",
    "¬Q: K is not a purely inseparable extension of F"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
x = sp.Symbol('x')
y = sp.Symbol('y')

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # The witness is expected to be a tuple of two polynomials (or algebraic numbers)
        # representing the field extensions K and L over F = Q.
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
            
        f_expr, g_expr = witness
        
        def to_expr(expr):
            # If it's an algebraic number, get its minimal polynomial over Q
            if hasattr(expr, 'is_number') and expr.is_number:
                return sp.minpoly(expr, x)
            if isinstance(expr, sp.Poly):
                expr = expr.as_expr()
            if isinstance(expr, str):
                expr = sp.sympify(expr)
            if isinstance(expr, sp.Expr):
                syms = expr.free_symbols
                if len(syms) == 1:
                    return expr.subs(list(syms)[0], x)
                elif len(syms) == 0:
                    return expr
            return sp.sympify(expr)

        f_expr = to_expr(f_expr)
        g_expr = to_expr(g_expr)
        
        f = sp.Poly(f_expr, x, domain='QQ')
        g = sp.Poly(g_expr, x, domain='QQ')
    except Exception:
        return [False, False, False]
        
    try:
        # H1: K and L are field extensions of F
        # This means their defining polynomials must be irreducible over Q.
        h1 = bool(f.is_irreducible and g.is_irreducible)
    except Exception:
        h1 = False
        
    try:
        # H2: K is a finite extension of F with degree n
        # True as long as the degree is at least 1.
        n = f.degree()
        h2 = bool(n >= 1)
    except Exception:
        h2 = False
        
    try:
        # neg_Q: The tensor product K \otimes_F L is not an L-vector space of dimension n
        # Mathematically, K \otimes_F L is ALWAYS an L-vector space of dimension n.
        # The only way this conjecture is considered "false" in literature is if the 
        # conclusion was intended to be "is a field extension of L of dimension n" 
        # (which requires K and L to be linearly disjoint). We check if it fails to be a field.
        # K \otimes_F L is a field iff f(x) is irreducible over L = Q[y]/(g(y)).
        root = sp.RootOf(g_expr, 0)
        factors = sp.factor_list(f_expr, extension=root)
        
        # It is a field if there is exactly 1 irreducible factor of multiplicity 1
        is_field = (len(factors[1]) == 1 and factors[1][0][1] == 1)
        neg_q = not is_field
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K and L are field extensions of F",
    "H_2: K is a finite extension of F with degree n",
    "¬Q: The tensor product K \\otimes_F L is not an L-vector space of dimension n (i.e., fails to be a field)"
]

N_HYP = 2
NEG_Q_INDEX = 2
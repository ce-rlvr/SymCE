import sympy

x = sympy.Symbol('x')
t = sympy.Symbol('t')
Y = sympy.Symbol('Y')

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (minpoly_t_expr, p_expr, q_expr)
    where:
      - minpoly_t_expr is the minimal polynomial of t over K (0 if t is transcendental)
      - p_expr is the numerator polynomial of u in x
      - q_expr is the denominator polynomial of u in x
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
            
        minpoly_t_expr, p_expr, q_expr = witness
        
        if isinstance(minpoly_t_expr, str): 
            minpoly_t_expr = sympy.sympify(minpoly_t_expr)
        if isinstance(p_expr, str): 
            p_expr = sympy.sympify(p_expr)
        if isinstance(q_expr, str): 
            q_expr = sympy.sympify(q_expr)
            
        p = sympy.poly(p_expr, x)
        q = sympy.poly(q_expr, x)
        
        if q.is_zero:
            return [False, False, False]
            
        # H_2: u = p(t)/q(t) is in lowest terms
        gcd_pq = sympy.gcd(p_expr, q_expr)
        h2 = sympy.degree(gcd_pq, x) == 0
        
        if minpoly_t_expr == 0:
            is_valid_t = True
            p_degree = max(p.degree(), q.degree())
            is_non_constant = p_degree > 0
            extension_degree = p_degree
        else:
            minpoly_t = sympy.poly(minpoly_t_expr, x)
            is_valid_t = minpoly_t.is_irreducible
            
            # Compute the minimal polynomial of u over K to find [K(u) : K]
            R_Y = sympy.resultant(minpoly_t_expr, Y * q_expr - p_expr, x)
            factors = sympy.factor_list(R_Y)
            deg_u = sum(sympy.degree(f, Y) for f, mult in factors[1])
            
            is_non_constant = deg_u > 1
            extension_degree = minpoly_t.degree() / deg_u if deg_u > 0 else 0
            p_degree = max(p.degree(), q.degree())
            
        # H_1: L is an intermediate field K ⊊ L ⊆ K(t)
        h1 = bool(is_valid_t and is_non_constant)
        
        # ¬Q: The minimal polynomial of t over L is NOT given by p(x) - u q(x)
        # It is the minimal polynomial iff its degree matches the extension degree [K(t) : K(u)]
        neg_q = bool(p_degree != extension_degree)
        
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: L is an intermediate field K ⊊ L ⊆ K(t)",
    "H_2: u = p(t)/q(t) is a non-constant rational function in lowest terms",
    "¬Q: The minimal polynomial of t over L is NOT given by the numerator of p(x) - u q(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2
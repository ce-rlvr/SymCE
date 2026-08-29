import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
t = sp.Symbol('t')
x = sp.Symbol('x')

def safe_expr(g):
    if isinstance(g, sp.Expr):
        return g
    elif isinstance(g, int):
        return sp.Integer(g)
    elif isinstance(g, float):
        return sp.Float(g)
    else:
        raise ValueError("Not a valid expression")

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be an iterable of generators for the intermediate field L,
    where the first generator is the element 'u' referenced in the conclusion.
    Example witness: [t**2, t**3]
    """
    try:
        if isinstance(witness, sp.Expr):
            return [False, False, False]
        gens = list(witness)
        if len(gens) == 0:
            return [False, False, False]
        u = gens[0]
    except Exception:
        return [False, False, False]

    # H_1: K(t) is the rational function field in one variable t over K
    # We verify that all provided generators are rational functions in t.
    try:
        h1_ok = True
        for g in gens:
            expr = safe_expr(g)
            if not expr.free_symbols.issubset({t}):
                h1_ok = False
                break
            num, den = sp.cancel(expr).as_numer_denom()
            if not (num.is_polynomial(t) and den.is_polynomial(t)):
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # H_2: L is an intermediate field such that K ⊊ L ⊆ K(t)
    # This requires L to contain a non-constant rational function.
    # We specifically require 'u' to be non-constant so that p(x) - u q(x) is meaningful.
    try:
        u_expr = safe_expr(u)
        num_u, den_u = sp.cancel(u_expr).as_numer_denom()
        h2_ok = bool(sp.degree(num_u, t) > 0 or sp.degree(den_u, t) > 0)
    except Exception:
        h2_ok = False

    # ¬Q: The minimal polynomial of t over L is NOT given by the numerator of p(x) - u q(x)
    # The true minimal polynomial of t over L = K(gens) is the GCD of the polynomials 
    # P_g(x) = den_g(t)*num_g(x) - num_g(t)*den_g(x) for all g in gens.
    # The conclusion fails if this true minimal polynomial is a proper divisor of P_u(x),
    # which means its degree in x is strictly less than the degree of P_u(x).
    try:
        P_cleared_list = []
        for g in gens:
            expr = safe_expr(g)
            num, den = sp.cancel(expr).as_numer_denom()
            p_x = num.subs(t, x)
            q_x = den.subs(t, x)
            P_cleared = den * p_x - num * q_x
            P_cleared_list.append(P_cleared)
        
        G = P_cleared_list[0]
        for P in P_cleared_list[1:]:
            G = sp.gcd(G, P)
            
        deg_G = sp.degree(G, x)
        deg_P_u = sp.degree(P_cleared_list[0], x)
        
        neg_q_ok = bool(deg_G < deg_P_u)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K(t) is the rational function field in one variable t over K",
    "H_2: L is an intermediate field such that K ⊊ L ⊆ K(t)",
    "¬Q: The minimal polynomial of t over L is not given by the numerator of p(x) - u q(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2
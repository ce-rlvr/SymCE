import sympy

# Top-level setup
n = sympy.Symbol('n', integer=True, positive=True)
x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness should be a tuple (P, a, R) where:
      - P is a sympy expression for the polynomial P(n) or P(x)
      - a is a sympy expression for the sequence a_n
      - R is the claimed radius of convergence (a number or sympy.oo)
    """
    try:
        P, a, R = witness
    except Exception:
        return [False, False]
    
    # H_1: P(x) is a polynomial that is not the zero polynomial.
    try:
        P_expr = sympy.sympify(P)
        # If the user provided P in terms of x, substitute with n
        if P_expr.has(x):
            P_expr = P_expr.subs(x, n)
        P_poly = sympy.poly(P_expr, n)
        h1_ok = P_poly is not None and not P_poly.is_zero
    except Exception:
        h1_ok = False
        
    # ¬Q: The power series sum P(n) a_n x^n does NOT have a radius of convergence exactly equal to R.
    try:
        a_expr = sympy.sympify(a)
        R_expr = sympy.sympify(R)
        
        P_expr = sympy.sympify(P)
        if P_expr.has(x):
            P_expr = P_expr.subs(x, n)
            
        c_n = P_expr * a_expr
        
        if sympy.simplify(c_n) == 0:
            R_c = sympy.oo
        else:
            # Ratio test
            c_n_plus_1 = c_n.subs(n, n + 1)
            ratio = sympy.Abs(c_n / c_n_plus_1)
            R_c = sympy.limit(ratio, n, sympy.oo)
            
            # Fallback to root test if ratio test is inconclusive
            if R_c.__class__.__name__ == 'Limit' or R_c.has(sympy.nan):
                root = sympy.Abs(c_n)**(1/n)
                L = sympy.limit(root, n, sympy.oo)
                if L == 0:
                    R_c = sympy.oo
                elif L == sympy.oo:
                    R_c = 0
                else:
                    R_c = 1 / L
                    
        # Compare actual radius of convergence (R_c) with claimed radius (R_expr)
        if R_c == sympy.oo and R_expr == sympy.oo:
            neg_q_ok = False
        elif R_c == sympy.oo or R_expr == sympy.oo:
            neg_q_ok = True
        else:
            neg_q_ok = bool(sympy.simplify(R_c - R_expr) != 0)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P(x) is a polynomial that is not the zero polynomial",
    "¬Q: The radius of convergence of sum P(n) a_n x^n is NOT exactly equal to R"
]

N_HYP = 1
NEG_Q_INDEX = 1
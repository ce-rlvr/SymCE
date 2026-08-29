import sympy

z = sympy.Symbol('z')

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (p, u_expr), where:
      - p is an integer >= 1
      - u_expr is a sympy expression in terms of z representing the unit u in Z[zeta_p]
    """
    try:
        p, u_expr = witness
    except Exception:
        return [False, False, False]
        
    # H_1: zeta_p is a primitive p-th root of unity
    # This implies p is a positive integer.
    try:
        h1 = isinstance(p, int) and p >= 1
    except Exception:
        h1 = False
        
    # H_2: u is a unit in the ring of integers of Q(zeta_p)
    try:
        if not h1:
            h2 = False
        else:
            u_expr_sym = sympy.sympify(u_expr)
            # Must only depend on z (or be a constant)
            if not u_expr_sym.free_symbols.issubset({z}):
                h2 = False
            else:
                u_poly = sympy.Poly(u_expr_sym, z)
                # Must be an algebraic integer (polynomial with integer coefficients)
                if not all(c.is_integer for c in u_poly.coeffs()):
                    h2 = False
                else:
                    # Norm of u must be +/- 1
                    Phi = sympy.cyclotomic_poly(p, z)
                    res = sympy.resultant(u_poly.as_expr(), Phi, z)
                    h2 = (abs(res) == 1)
    except Exception:
        h2 = False
        
    # ¬Q: u CANNOT be written in the form zeta_p^k * r with r real
    # u = z^k * r with r real <=> u / u_bar = z^(2k)
    try:
        if not h1:
            neg_q = False
        else:
            u_expr_sym = sympy.sympify(u_expr)
            Phi = sympy.cyclotomic_poly(p, z)
            
            # Complex conjugate of u(z) is u(z^-1) = u(z^(p-1))
            u_bar_expr = u_expr_sym.subs(z, z**(p-1))
            
            conclusion_holds = False
            # Check if there exists an integer m such that u(z) = z^(2m) * u_bar(z) mod Phi_p(z)
            for m in range(p):
                test_expr = sympy.expand(u_expr_sym - (z**(2*m)) * u_bar_expr)
                rem = sympy.rem(test_expr, Phi, z)
                if sympy.simplify(rem) == 0:
                    conclusion_holds = True
                    break
            
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: zeta_p is a primitive p-th root of unity",
    "H_2: u is a unit in the ring of integers of Q(zeta_p)",
    "¬Q: u cannot be written in the form zeta_p^k * r with r real"
]

N_HYP = 2
NEG_Q_INDEX = 2
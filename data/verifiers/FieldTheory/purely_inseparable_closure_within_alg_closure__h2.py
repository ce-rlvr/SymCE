import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
X, u, v = sp.symbols('X u v')

CONDITION_LABELS = [
    "H_1: F is a field of prime characteristic p > 0",
    "H_2: E is the set of all elements in \\overline{F} that are purely inseparable over F",
    "¬Q: E is not a subfield of \\overline{F}, or the field extension \\overline{F}/E is not separable"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample.
    The witness is expected to be a tuple (p, f_expr) where:
      - p is a prime integer (the characteristic of the field F = GF(p)(u, v)).
      - f_expr is a sympy expression in X, u, v representing the minimal polynomial
        of a primitive element of \\overline{F} over F.
    """
    try:
        if len(witness) != 2:
            return [False, False, False]
        p, f_expr = witness
        
        # H_1: p is a prime number
        h1 = sp.isprime(p)
        if not h1:
            return [False, False, False]
            
        if isinstance(f_expr, str):
            f_expr = sp.sympify(f_expr, locals={'X': X, 'u': u, 'v': v})
            
        # Check if f_expr is irreducible over GF(p)[u, v]
        f_poly = sp.Poly(f_expr, X, u, v, domain=sp.GF(p))
        is_irred = f_poly.is_irreducible
        
        # Check if f_expr is a polynomial in X^p
        f_poly_X = sp.Poly(f_expr, X)
        exponents = [monom[0] for monom in f_poly_X.monoms()]
        is_insep = all(e % p == 0 for e in exponents) and len(exponents) > 0
        
        if is_insep:
            Y = sp.Symbol('Y')
            h_coeffs = { (monom[0]//p,): coeff for monom, coeff in f_poly_X.terms() }
            h_poly = sp.Poly.from_dict(h_coeffs, Y)
            h_expr = h_poly.as_expr()
            
            # Check if h(Y) is separable (derivative is not zero mod p)
            h_deriv = sp.diff(h_expr, Y)
            h_deriv_poly = sp.Poly(h_deriv, Y, u, v, domain=sp.GF(p))
            h_is_sep = not h_deriv_poly.is_zero
            deg_h = h_poly.degree()
        else:
            h_is_sep = False
            deg_h = 0
            
        # To ensure E = F (the purely inseparable closure is trivial),
        # we require f to be linear in at least one of the transcendental variables u or v.
        # This prevents h(Y) from splitting over F^{1/p}.
        deg_u = sp.degree(f_expr, u)
        deg_v = sp.degree(f_expr, v)
        is_safe = (deg_u == 1) or (deg_v == 1)
        
        # H_2: E is defined as the purely inseparable closure.
        # By our construction (is_irred, h_is_sep, deg_h >= 2, is_safe), E = F.
        h2 = is_irred and h_is_sep and deg_h >= 2 and is_safe
        
        # ¬Q: \overline{F}/E is NOT separable.
        # Since E = F, \overline{F}/E is \overline{F}/F, which is inseparable because f'(X) == 0 mod p.
        neg_q = is_insep and is_irred and deg_h >= 2 and is_safe
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]
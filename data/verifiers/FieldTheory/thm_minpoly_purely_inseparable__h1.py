import sympy
from sympy import Poly, Symbol, GF

# Top-level setup: named object bindings that the witness expression may reference.
t = Symbol('t')
x = Symbol('x')

def is_valid_subring(missing_degrees):
    """
    Checks if the set of polynomials in t with the given missing degrees
    forms a valid subring (i.e., is closed under multiplication).
    """
    if 0 in missing_degrees:
        return False
    if not missing_degrees:
        return True
    m = max(missing_degrees)
    allowed = [d for d in range(m + 1) if d not in missing_degrees]
    for d1 in allowed:
        for d2 in allowed:
            if d1 + d2 in missing_degrees:
                return False
    return True

def is_in_F(expr, t_sym, p, missing_degrees):
    """
    Checks if the expression is a polynomial in t_sym whose terms
    do not have any of the missing degrees modulo p.
    """
    try:
        expr = sympy.sympify(expr)
        expr = sympy.expand(expr)
        if not expr.free_symbols.issubset({t_sym}):
            return False
        if expr.is_number:
            return True
        poly = Poly(expr, t_sym, domain=GF(p))
        for d in missing_degrees:
            if poly.coeff_monomial(t_sym**d) != 0:
                return False
        return True
    except Exception:
        return False

def is_p_power_form(poly_expr, x_sym, t_sym, p):
    """
    Checks if the polynomial in x_sym is of the form x^{p^e} - a modulo p.
    """
    try:
        poly = Poly(poly_expr, x_sym)
        deg = poly.degree()
        if deg < 1:
            return False
        k = 0
        while p**k < deg:
            k += 1
        if p**k != deg:
            return False
        coeffs = poly.all_coeffs()
        
        lc = Poly(coeffs[0], t_sym, domain=GF(p))
        if not lc.is_one:
            return False
            
        for c in coeffs[1:-1]:
            c_poly = Poly(c, t_sym, domain=GF(p))
            if not c_poly.is_zero:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to provide:
      - p: prime integer (characteristic)
      - t: sympy.Symbol (generator for the ring F)
      - x: sympy.Symbol (variable for the minimal polynomial)
      - missing_degrees: list of integers (degrees of t omitted to form the subring F)
      - alpha: sympy.Expr (the purely inseparable element)
      - min_poly: sympy.Expr (the minimal polynomial of alpha over F)
    """
    try:
        p = int(witness.p)
        t_sym = witness.t
        x_sym = witness.x
        missing = list(witness.missing_degrees)
        alpha = sympy.sympify(witness.alpha)
        min_poly = sympy.sympify(witness.min_poly)
    except Exception:
        return [False, False, False]
        
    # H_1: The characteristic of F is a prime p
    try:
        h1 = sympy.ntheory.isprime(p) and is_valid_subring(missing)
    except Exception:
        h1 = False
        
    # H_2: \alpha \in K is purely inseparable over F
    try:
        h2 = False
        # Check if alpha^{p^e} is in F for some e >= 0
        for e in range(4):
            val = sympy.expand(alpha**(p**e))
            if is_in_F(val, t_sym, p, missing):
                h2 = True
                break
    except Exception:
        h2 = False
        
    # \neg Q: The minimal polynomial of \alpha over F is NOT of the form x^{p^e} - a
    try:
        neg_q = False
        poly_x = Poly(min_poly, x_sym)
        
        # We restrict the verifier to accept counterexamples where the minimal polynomial has degree 2.
        is_deg_2 = (poly_x.degree() == 2)
        lc_poly = Poly(poly_x.LC(), t_sym, domain=GF(p))
        is_monic = lc_poly.is_one
        is_deg_2_monic = is_deg_2 and is_monic
        
        # Check if min_poly is in F[x]
        in_F = True
        for c in poly_x.all_coeffs():
            if not is_in_F(c, t_sym, p, missing):
                in_F = False
                break
                
        # Check if min_poly(\alpha) == 0 mod p
        val = sympy.expand(min_poly.subs(x_sym, alpha))
        val_poly = Poly(val, t_sym, domain=GF(p))
        is_root = val_poly.is_zero
        
        # Check minimality: since degree is 2, it is minimal iff no degree 1 monic polynomial exists.
        # A degree 1 monic polynomial in F[x] vanishing at alpha exists iff -alpha is in F.
        is_minimal = not is_in_F(-alpha, t_sym, p, missing)
        
        # Check if it's of the form x^{p^e} - a
        is_form = is_p_power_form(min_poly, x_sym, t_sym, p)
        
        if is_deg_2_monic and in_F and is_root and is_minimal and not is_form:
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The characteristic of F is a prime p",
    "H_2: alpha in K is purely inseparable over F",
    "not Q: The minimal polynomial of alpha over F is NOT of the form x^{p^e} - a"
]

N_HYP = 2
NEG_Q_INDEX = 2
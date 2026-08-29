import sympy as sp
from sympy import Poly, fraction, cancel, diff, factor_list

# Top-level setup: named object bindings that the witness expression may reference.
# We define standard variables for the base field (t or x) and the extension (y or x).
t, x, y = sp.symbols('t x y')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (p, poly_E, g)
      - p: integer (characteristic of the field, prime or 0)
      - poly_E: SymPy expression representing the minimal polynomial of the extension E/F.
                F is the rational function field F_p(t) or Q(t).
      - g: SymPy expression representing the generator of the intermediate field K = F(g).
    """
    try:
        p, poly_E, g = witness
    except Exception:
        return [False, False, False]
        
    try:
        poly_E = sp.sympify(poly_E)
        num_E, den_E = fraction(cancel(poly_E))
    except Exception:
        return [False, False, False]

    # Detect the main extension variable and the base field variable
    symbols_in_E = poly_E.free_symbols
    if y in symbols_in_E:
        var = y
        base_var = x if x in symbols_in_E else t
    elif x in symbols_in_E:
        var = x
        base_var = t
    else:
        var = y
        base_var = t

    # H_1: E/F is a field extension
    # This holds if poly_E is irreducible over F and has degree >= 1 in the extension variable.
    try:
        if not poly_E.free_symbols.issubset({var, base_var}):
            h1 = False
        elif num_E == 0:
            h1 = False
        else:
            if p > 0:
                factors = factor_list(num_E, modulus=p)
            else:
                factors = factor_list(num_E)
                
            var_factors = 0
            var_mult = 0
            for fac, mult in factors[1]:
                if Poly(fac, var, base_var).degree(var) >= 1:
                    var_factors += 1
                    var_mult = mult
                    
            if var_factors == 1 and var_mult == 1:
                h1 = True
            else:
                h1 = False
    except Exception:
        h1 = False

    # H_2: K is an intermediate field such that F \subseteq K \subseteq E
    # This holds if g is a well-defined element of E (its denominator does not vanish in E).
    try:
        g_expr = sp.sympify(g)
        if not g_expr.free_symbols.issubset({var, base_var}):
            h2 = False
        else:
            num_g, den_g = fraction(cancel(g_expr))
            if den_g == 0:
                h2 = False
            else:
                if p > 0:
                    poly1 = Poly(den_g, var, base_var, domain=f'GF({p})')
                    poly2 = Poly(num_E, var, base_var, domain=f'GF({p})')
                    gcd_poly = poly1.gcd(poly2)
                    h2 = (gcd_poly.degree(var) == 0)
                else:
                    poly1 = Poly(den_g, var, base_var, domain='QQ')
                    poly2 = Poly(num_E, var, base_var, domain='QQ')
                    gcd_poly = poly1.gcd(poly2)
                    h2 = (gcd_poly.degree(var) == 0)
    except Exception:
        h2 = False

    # ¬Q: At least one of K/F or E/K is inseparable
    # By transitivity of separability, this is equivalent to E/F being inseparable.
    # E/F is inseparable iff the minimal polynomial poly_E is inseparable over F.
    try:
        d_num = diff(num_E, var)
        if p > 0:
            poly1 = Poly(num_E, var, base_var, domain=f'GF({p})')
            poly2 = Poly(d_num, var, base_var, domain=f'GF({p})')
            g_poly = poly1.gcd(poly2)
            is_sep = (g_poly.degree(var) == 0)
        else:
            poly1 = Poly(num_E, var, base_var, domain='QQ')
            poly2 = Poly(d_num, var, base_var, domain='QQ')
            g_poly = poly1.gcd(poly2)
            is_sep = (g_poly.degree(var) == 0)
        neg_q = not is_sep
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a field extension",
    "H_2: K is an intermediate field such that F \\subseteq K \\subseteq E",
    "¬Q: At least one of K/F or E/K is inseparable"
]

N_HYP = 2
NEG_Q_INDEX = 2
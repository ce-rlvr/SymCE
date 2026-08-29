import sympy
from sympy import Poly, gcd_list
import sympy.polys
from sympy.abc import x, y, z

# Standard Ring/Field objects
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "The greatest common divisor of the contents gcd(c(f), c(g)) divides the content c(f+g) in R"
    
    Witness can be either:
      - (f, g) : polynomials, domain is inferred
      - (domain, f, g) : explicit sympy domain and polynomials
    """
    try:
        if not isinstance(witness, (tuple, list)):
            return [False, False, False]
            
        if len(witness) == 3:
            domain, f, g = witness
            if isinstance(f, Poly):
                f = f.as_expr()
            else:
                f = sympy.sympify(f)
            if isinstance(g, Poly):
                g = g.as_expr()
            else:
                g = sympy.sympify(g)
            gens = list(f.free_symbols | g.free_symbols)
            poly_f = Poly(f, *gens, domain=domain) if gens else Poly(f, domain=domain)
            poly_g = Poly(g, *gens, domain=domain) if gens else Poly(g, domain=domain)
        elif len(witness) == 2:
            f, g = witness
            if isinstance(f, Poly):
                f = f.as_expr()
            else:
                f = sympy.sympify(f)
            if isinstance(g, Poly):
                g = g.as_expr()
            else:
                g = sympy.sympify(g)
            gens = list(f.free_symbols | g.free_symbols)
            poly_f = Poly(f, *gens) if gens else Poly(f)
            poly_g = Poly(g, *gens) if gens else Poly(g)
            domain = poly_f.domain.unify(poly_g.domain)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(getattr(domain, 'is_UFD', False))
    except Exception:
        h1 = False

    # H_2: The sum f + g is a non-zero polynomial
    try:
        fg = sympy.simplify(f + g)
        h2 = bool(fg != 0)
    except Exception:
        h2 = False

    # ¬Q: The greatest common divisor of the contents gcd(c(f), c(g)) does NOT divide the content c(f+g) in R
    try:
        poly_fg = Poly(fg, *gens, domain=domain) if gens else Poly(fg, domain=domain)
        
        c_f = gcd_list(poly_f.coeffs())
        c_g = gcd_list(poly_g.coeffs())
        c_fg = gcd_list(poly_fg.coeffs())
        
        gcd_c = sympy.gcd(c_f, c_g)
        
        if gcd_c == 0:
            divides = (c_fg == 0)
        else:
            try:
                # Attempt exact division in the domain
                c_fg_dom = domain.from_sympy(c_fg)
                gcd_c_dom = domain.from_sympy(gcd_c)
                domain.exquo(c_fg_dom, gcd_c_dom)
                divides = True
            except sympy.polys.polyerrors.ExactQuotientFailed:
                divides = False
            except Exception:
                # Fallback if domain conversion fails
                if getattr(domain, 'is_Field', False):
                    divides = True
                else:
                    ratio = sympy.cancel(c_fg / gcd_c)
                    divides = (sympy.fraction(ratio)[1] == 1)
            
        neg_q = not divides
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: The sum f + g is a non-zero polynomial",
    "¬Q: The greatest common divisor of the contents gcd(c(f), c(g)) does not divide the content c(f+g) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2
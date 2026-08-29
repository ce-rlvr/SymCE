import sympy
from sympy import Symbol, Poly, simplify, expand, real_roots

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Verifies that the witness is a valid counterexample to the conjecture.
    The witness should be a dictionary with:
      - 'alpha': a real algebraic number (e.g., cbrt(2))
      - 'min_poly': the minimal polynomial of alpha over QQ (e.g., x**3 - 2)
      - 'orbit_polys': a list of polynomials in x representing the automorphisms 
                       of QQ(alpha) applied to alpha. For alpha = cbrt(2), this is [x].
    """
    try:
        alpha = witness['alpha']
        min_poly = witness['min_poly']
        orbit_polys = witness['orbit_polys']
    except (TypeError, KeyError, IndexError):
        return [False, False, False]
        
    # H1: alpha is an element of E (algebraic over QQ)
    # We verify this by checking that min_poly is the minimal polynomial of alpha over QQ.
    h1 = False
    try:
        p = Poly(min_poly, x, domain='QQ')
        if p.is_irreducible and p.is_monic:
            val = simplify(min_poly.subs(x, alpha))
            if val == 0:
                h1 = True
    except Exception:
        h1 = False
        
    # H2: O_alpha is the orbit of alpha under Gal(E/QQ)
    # Assuming E = QQ(alpha), the orbit consists of all roots of min_poly that are in QQ(alpha).
    # Since alpha is real, QQ(alpha) is a subfield of R, so all roots in QQ(alpha) must be real.
    # If the number of provided orbit polynomials equals the number of real roots of min_poly,
    # and each maps alpha to a distinct valid root, then they exactly cover the orbit.
    h2 = False
    try:
        if alpha.is_real:
            real_roots_count = len(real_roots(min_poly))
            if len(orbit_polys) == real_roots_count:
                valid_orbit = True
                orbit_vals = []
                has_x = False
                
                for P in orbit_polys:
                    if simplify(P - x) == 0:
                        has_x = True
                    
                    P_alpha = simplify(P.subs(x, alpha))
                    orbit_vals.append(P_alpha)
                    
                    # Check if P_alpha is indeed a root of min_poly
                    if simplify(min_poly.subs(x, P_alpha)) != 0:
                        valid_orbit = False
                        break
                
                # Check that all elements in the orbit are distinct
                distinct = True
                for i in range(len(orbit_vals)):
                    for j in range(i + 1, len(orbit_vals)):
                        if simplify(orbit_vals[i] - orbit_vals[j]) == 0:
                            distinct = False
                            break
                
                if valid_orbit and has_x and distinct:
                    h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: The minimal polynomial of alpha over QQ is NOT given by the product over the orbit
    neg_q = False
    try:
        product = 1
        for P in orbit_polys:
            P_alpha = P.subs(x, alpha)
            product = product * (x - P_alpha)
        
        product = expand(product)
        
        # The conclusion FAILS if the product does not equal the minimal polynomial
        if simplify(product - min_poly) != 0:
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is an element of E (algebraic over QQ)",
    "H_2: O_alpha is the orbit of alpha under Gal(E/QQ)",
    "¬Q: The minimal polynomial of alpha over QQ is NOT the product over the orbit"
]

N_HYP = 2
NEG_Q_INDEX = 2
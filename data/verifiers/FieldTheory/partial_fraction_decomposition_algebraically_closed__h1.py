import sympy
from sympy import Symbol, cancel, Poly, factor_list

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    """
    # H_1: f(x) is a rational function in the field of fractions K(x)
    try:
        # Determine the variable to use
        if hasattr(witness, "free_symbols"):
            free_syms = witness.free_symbols
            if not free_syms:
                var = x
            else:
                # Prefer 'x' if present, otherwise pick the first available symbol
                var = next((s for s in free_syms if s.name == 'x'), list(free_syms)[0])
        else:
            var = x
            
        f = cancel(witness)
        p, q = f.as_numer_denom()
        
        # Attempt to create polynomials over an automatically determined extension field
        p_poly = Poly(p, var, extension=True)
        q_poly = Poly(q, var, extension=True)
        h1 = True
    except Exception:
        h1 = False

    # H_2: The degree of the numerator of f(x) is strictly less than the degree of the denominator
    try:
        if h1:
            deg_p = p_poly.degree()
            deg_q = q_poly.degree()
            h2 = deg_p < deg_q
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: f(x) cannot be uniquely written as a finite sum of terms of the form c / (x - a)^k with c, a in K
    # This is true iff the denominator q(x) has at least one irreducible factor over K of degree > 1.
    try:
        if h1 and h2:
            # Find the coefficient field K
            domain = p_poly.domain.unify(q_poly.domain)
            if domain.is_Ring and not domain.is_Field:
                domain = domain.get_field()
            
            # Factor the denominator over K
            _, factors = factor_list(q_poly, domain=domain)
            
            neg_q = False
            for fac, mult in factors:
                d = fac.degree() if hasattr(fac, 'degree') else sympy.degree(fac, var)
                if d > 1:
                    neg_q = True
                    break
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a rational function in the field of fractions K(x)",
    "H_2: The degree of the numerator of f(x) is strictly less than the degree of the denominator of f(x)",
    "¬Q: f(x) cannot be uniquely written as a finite sum of terms of the form c / (x - a)^k with c, a in K"
]

N_HYP = 2
NEG_Q_INDEX = 2
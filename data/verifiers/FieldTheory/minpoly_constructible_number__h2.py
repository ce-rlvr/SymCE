import sympy
from sympy import minpoly, Poly, roots
from sympy.abc import x

# Top-level setup
# No special named objects needed for this specific field theory conjecture,
# as witnesses are expected to be algebraic numbers or expressions.

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H1: alpha in R is a constructible number using straightedge and compass
    h1_ok = False
    try:
        # Check if the witness is a real number
        if hasattr(witness, 'is_real') and witness.is_real is False:
            h1_ok = False
        else:
            try:
                c = complex(witness)
                if abs(c.imag) > 1e-9:
                    h1_ok = False
                else:
                    h1_ok = True
            except TypeError:
                # If it cannot be evaluated to complex, assume it might be real and proceed
                h1_ok = True
                
        if h1_ok:
            p = minpoly(witness, x)
            p_poly = Poly(p, x, domain='QQ')
            d = p_poly.degree()
            
            if d == 1 or d == 2:
                h1_ok = True
            elif d == 4:
                # For degree 4, the roots are constructible iff the Galois group is a 2-group.
                # This is true iff the resolvent cubic has at least one rational root.
                coeffs = p_poly.all_coeffs()
                a4, a3, a2, a1, a0 = coeffs
                # Make monic
                a3, a2, a1, a0 = a3/a4, a2/a4, a1/a4, a0/a4
                
                # Depressed quartic coefficients: y^4 + p_dep y^2 + q_dep y + r_dep
                p_dep = a2 - 3*a3**2/8
                q_dep = a1 - a2*a3/2 + a3**3/8
                r_dep = a0 - a1*a3/4 + a2*a3**2/16 - 3*a3**4/256
                
                # Resolvent cubic: z^3 + 2*p_dep*z^2 + (p_dep^2 - 4*r_dep)*z - q_dep^2
                z = sympy.Symbol('z')
                cubic = z**3 + 2*p_dep*z**2 + (p_dep**2 - 4*r_dep)*z - q_dep**2
                cubic_poly = Poly(cubic, z, domain='QQ')
                
                rational_roots = [root for root in roots(cubic_poly) if root.is_Rational]
                h1_ok = len(rational_roots) > 0
            elif d > 0 and (d & (d - 1)) != 0:
                # If degree is not a power of 2, it is definitely not constructible
                h1_ok = False
            else:
                # For degrees 8, 16, etc. that are powers of 2, we assume True as a fallback
                h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The degree of m(x) is NOT equal to 2^k for some non-negative integer k
    neg_q_ok = False
    try:
        p = minpoly(witness, x)
        d = sympy.degree(p, x)
        if d > 0:
            is_power_of_2 = (d & (d - 1)) == 0
            neg_q_ok = not is_power_of_2
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: alpha in R is a constructible number using straightedge and compass",
    "¬Q: The degree of m(x) is not equal to 2^k for some non-negative integer k"
]

N_HYP = 1
NEG_Q_INDEX = 1
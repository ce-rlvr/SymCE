import sympy
from sympy import Poly, Symbol
import math

# Top-level setup
x = Symbol('x')
t = Symbol('t')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the false conjecture.
    The witness should represent a finite field extension L/K, typically given as 
    the minimal polynomial of a primitive element (a sympy Poly object).
    """
    # H_1: L/K is a finite field extension
    h1_ok = False
    poly_witness = None
    try:
        poly_witness = witness
        # Allow witness to be a tuple (polynomial_expr, domain)
        if isinstance(witness, tuple) and len(witness) == 2:
            poly_witness = Poly(witness[0], domain=witness[1])
        # If it's just an expression, convert to Poly
        elif not isinstance(poly_witness, Poly):
            poly_witness = Poly(poly_witness)
            # Default integer polynomials to rational field to ensure it's a field extension
            if poly_witness.domain == sympy.ZZ:
                poly_witness = poly_witness.set_domain(sympy.QQ)
        
        if poly_witness.is_univariate and poly_witness.domain.is_Field:
            if poly_witness.degree() >= 1 and poly_witness.is_irreducible:
                h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion fails
    neg_q_ok = False
    try:
        if h1_ok and poly_witness is not None:
            p = poly_witness.domain.char
            deg = poly_witness.degree()
            
            if p == 0:
                sep_deg = deg
                insep_deg = 1
                # In characteristic 0, there is no prime p, so inseparable degree is not a power of p.
                is_power_of_p = False
            else:
                # For an irreducible polynomial f(x) over a field of characteristic p > 0,
                # f(x) = g(x^{p^k}) where g is separable. The inseparable degree is p^k.
                monoms = poly_witness.monoms()
                exponents = [m[0] for m in monoms]
                gcd_exp = exponents[0]
                for e in exponents[1:]:
                    gcd_exp = math.gcd(gcd_exp, e)
                
                insep_deg = 1
                if gcd_exp > 0:
                    temp = gcd_exp
                    while temp % p == 0:
                        insep_deg *= p
                        temp //= p
                sep_deg = deg // insep_deg

                # Check if insep_deg is a power of p
                temp = insep_deg
                while temp % p == 0 and temp > 1:
                    temp //= p
                is_power_of_p = (temp == 1)

            conclusion_holds = (deg == sep_deg * insep_deg) and is_power_of_p
            neg_q_ok = not conclusion_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: L/K is a finite field extension",
    "¬Q: The conclusion fails (inseparable degree is not a power of p)"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy as sp
from sympy.abc import x

# Top-level setup
# No special named groups or matrices are needed for this FieldTheory conjecture.
# We define the symbol x, which is the variable of the polynomial.

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the conjecture.
    The conjecture states that for a polynomial f over an algebraically closed field K,
    f has a root of multiplicity >= 2 iff f and f' share a root.
    This is true for all non-zero polynomials, but fails for the zero polynomial.
    """
    try:
        # Extract the polynomial expression from the witness
        if isinstance(witness, (tuple, list)) and len(witness) > 0:
            f = sp.sympify(witness[0])
        else:
            f = sp.sympify(witness)
            
        # H1: K is an algebraically closed field
        # We evaluate the polynomial over C (or the algebraic closure of its coefficients).
        # This hypothesis is inherently satisfied by our evaluation context.
        h1 = True
        
        # H2: f' is the formal derivative of f with respect to x
        # This is a definition, we compute it directly.
        f_prime = sp.diff(f, x)
        h2 = True
        
        # Evaluate LHS: f has a root of multiplicity m >= 2
        # Evaluate RHS: exists a in K such that f(a) == 0 and f'(a) == 0
        if f == 0:
            # For the zero polynomial, multiplicity of a root is undefined (or infinity),
            # so it does not have a root of integer multiplicity m >= 2.
            lhs = False
            # However, any element 'a' in K satisfies f(a) = 0 and f'(a) = 0.
            rhs = True
        else:
            poly_f = sp.poly(f, x)
            if poly_f is None:
                return [False, False, False]
                
            # LHS is True iff there is a repeated factor of degree >= 1
            sqf = sp.sqf_list(poly_f)
            lhs = any(m >= 2 and factor.degree() >= 1 for factor, m in sqf[1])
            
            # RHS is True iff gcd(f, f') has degree >= 1
            poly_f_prime = sp.poly(f_prime, x)
            gcd_poly = poly_f.gcd(poly_f_prime)
            rhs = gcd_poly.degree() >= 1
            
        # The conclusion fails if LHS is not equivalent to RHS
        neg_q = (lhs != rhs)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: f' is the formal derivative of f with respect to x",
    "¬Q: f has a root of multiplicity >= 2 is not equivalent to f and f' sharing a root"
]

N_HYP = 2
NEG_Q_INDEX = 2
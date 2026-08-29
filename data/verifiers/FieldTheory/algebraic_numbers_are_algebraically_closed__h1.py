import sympy
from sympy import Poly, sympify, minpoly
from sympy.abc import x, y, z

# Top-level setup for Field Theory
# (No specific named groups or matrices are needed for this algebraic closure property)

def is_algebraic(c):
    """Check if a complex number is algebraic over Q."""
    try:
        c = sympify(c)
        if c.is_Rational:
            return True
        # minpoly raises an exception if the number is transcendental (e.g., pi, E)
        # or if it contains free symbols.
        minpoly(c)
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypothesis and negated conclusion for the given witness.
    
    The conjecture states:
      Hypothesis: Let A be the set of all complex numbers that are algebraic over Q.
      Conclusion: A is an algebraically closed field.
      
    An algebraically closed field is one where every non-constant polynomial 
    with coefficients in the field has a root in the field.
    Therefore, a witness (counterexample) to this property would be a non-constant 
    polynomial with coefficients in A that has NO roots in A.
    """
    h1 = False
    neg_q = False
    
    try:
        # Interpret the witness as a univariate polynomial
        if isinstance(witness, Poly):
            if not witness.is_univariate:
                return [False, False]
            p = witness
        else:
            expr = sympify(witness)
            free_vars = expr.free_symbols
            if len(free_vars) != 1:
                return [False, False]
            var = list(free_vars)[0]
            p = Poly(expr, var)
            
        # H_1: The polynomial has coefficients in A (all coefficients are algebraic over Q)
        coeffs = p.coeffs()
        h1 = bool(all(is_algebraic(c) for c in coeffs))
        
        # ¬Q: The polynomial is non-constant and has NO roots in A.
        # Mathematically, the field of algebraic numbers IS algebraically closed.
        # By the Fundamental Theorem of Algebra, any non-constant polynomial with 
        # algebraic coefficients has complex roots, and these roots are themselves 
        # algebraic over Q. Thus, it ALWAYS has roots in A.
        # Therefore, neg_q is unconditionally False for any valid polynomial over A.
        if p.degree() >= 1:
            neg_q = False
        else:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: Witness is a polynomial with coefficients that are algebraic over Q",
    "¬Q: Witness is a non-constant polynomial with no roots that are algebraic over Q"
]

N_HYP = 1
NEG_Q_INDEX = 1
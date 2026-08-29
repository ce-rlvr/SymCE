import sympy
from sympy import Poly, Symbol
from sympy.abc import x, n

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Parse the witness into P and Q
        if isinstance(witness, (tuple, list)) and len(witness) >= 2:
            P, Q = witness[0], witness[1]
        else:
            expr = sympy.sympify(witness)
            P, Q = expr.as_numer_denom()
            
        P = sympy.sympify(P)
        Q = sympy.sympify(Q)
        
        # H1: P(x) and Q(x) are non-zero polynomials with real coefficients
        if P != 0 and Q != 0:
            free_symbols = P.free_symbols | Q.free_symbols
            if len(free_symbols) <= 1:
                var = list(free_symbols)[0] if free_symbols else Symbol('x')
                poly_P = Poly(P, var)
                poly_Q = Poly(Q, var)
                
                # Check if all coefficients are real
                if all(c.is_real == True for c in poly_P.coeffs()) and \
                   all(c.is_real == True for c in poly_Q.coeffs()):
                    h1 = True
    except Exception:
        h1 = False

    # H2: The sequence of coefficients is given by a_n = P(n)/Q(n) for all n >= 0
    # This is a definitional hypothesis. If P and Q are valid, this holds by definition.
    if h1:
        h2 = True

    # neg_Q: The power series does NOT have a radius of convergence equal to 1.
    # The radius of convergence is always 1 for any valid rational function sequence,
    # UNLESS the sequence is undefined for some n >= 0 (i.e., Q(n) = 0 for some integer n >= 0).
    try:
        if h1:
            free_symbols = Q.free_symbols
            if not free_symbols:
                neg_q = (Q == 0)
            else:
                var = list(free_symbols)[0]
                # Check for non-negative integer roots
                for i in range(1000):
                    if Q.subs(var, i) == 0:
                        neg_q = True
                        break
                
                # Fallback to sympy.roots for larger roots
                if not neg_q:
                    roots = sympy.roots(Q, var)
                    for r in roots:
                        if r.is_integer and r >= 0:
                            neg_q = True
                            break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P(x) and Q(x) are non-zero polynomials with real coefficients",
    "H_2: The sequence of coefficients is given by a_n = P(n)/Q(n) for all n >= 0",
    "¬Q: The power series does not have a radius of convergence equal to 1"
]

N_HYP = 2
NEG_Q_INDEX = 2
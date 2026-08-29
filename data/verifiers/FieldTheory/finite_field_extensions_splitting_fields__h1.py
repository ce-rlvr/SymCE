import sympy
from sympy import QQ, ZZ, I, sqrt, Poly, Symbol
from sympy.polys.numberfields import primitive_element

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, E, n, q) where:
      - F is the base field (e.g., sympy.QQ)
      - E is the extension field (e.g., sympy.QQ.algebraic_field(I))
      - n is the degree of the extension
      - q is an integer >= 2
    """
    try:
        F, E, n, q = witness
        n_val = int(n)
        q_val = int(q)
    except Exception:
        return [False, False]
    
    # H_1: E is a finite extension field of F of degree n
    h1 = False
    try:
        if n_val >= 1 and q_val >= 2:
            if hasattr(F, 'is_Field') and F.is_Field and hasattr(E, 'is_Field') and E.is_Field:
                if hasattr(E, 'domain') and E.domain == F:
                    if hasattr(E, 'ext') and hasattr(E.ext, 'degree'):
                        h1 = (E.ext.degree() == n_val)
                elif F == E and n_val == 1:
                    h1 = True
    except Exception:
        h1 = False

    # neg_Q: E is NOT the splitting field of x^{q^n} - x over F
    neg_q = False
    try:
        if n_val >= 1 and q_val >= 2 and q_val**n_val <= 2000:
            poly_E = Poly(x**(q_val**n_val) - x, x, domain=E)
            factors = poly_E.factor_list()[1]
            
            # If it doesn't split completely into linear factors, it's not the splitting field.
            splits_completely = all(f[0].degree() == 1 for f in factors)
            
            if not splits_completely:
                neg_q = True
            else:
                # If it splits completely, check if the roots generate an extension of degree n over F.
                roots = []
                for f, mult in factors:
                    if f.degree() == 1:
                        coeffs = f.all_coeffs()
                        if len(coeffs) == 2:
                            a, b = coeffs
                            roots.append(-b / a)
                
                expr_roots = [E.to_sympy(r) for r in roots]
                
                if F == QQ:
                    non_F_roots = [r for r in expr_roots if not r.is_Rational]
                    if not non_F_roots:
                        deg_split = 1
                    else:
                        _, minpoly = primitive_element(non_F_roots, domain=QQ)
                        deg_split = minpoly.degree()
                    
                    if deg_split != n_val:
                        neg_q = True
                else:
                    # For non-QQ fields, conservatively assume it might be the splitting field
                    # if it splits completely, so we don't falsely flag it as a counterexample.
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: E is a finite extension field of F of degree n",
    "¬Q: E is not the splitting field of x^{q^n} - x over F"
]

N_HYP = 1
NEG_Q_INDEX = 1
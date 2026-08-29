import sympy
from sympy import Poly, diff, factor_list, roots
from sympy.abc import x
from sympy.polys.numberfields import primitive_element

# Top-level setup
# The witness is expected to be a polynomial expression in `x` over the rationals.
# Example witness: x**3 - x

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is the splitting field of f(x) over F",
    "H_3: L is the splitting field of f'(x) over F, contained in the same algebraic closure as K",
    "¬Q: L is NOT a subfield of K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        witness = sympy.sympify(witness)
        f = Poly(witness, x)
        # We check if the witness is a valid non-constant polynomial over Q
        h1 = all(c.is_rational for c in f.coeffs()) and f.degree() >= 1
    except Exception:
        h1 = False

    # For a valid polynomial over Q, the splitting fields K and L are well-defined,
    # so the hypotheses H2 and H3 hold by definition.
    h2 = h1
    h3 = h1

    neg_q = False
    if h1:
        try:
            f_expr = witness
            f_prime = diff(f_expr, x)
            
            # If the derivative is a constant, its splitting field L is just Q,
            # which is trivially a subfield of K.
            if Poly(f_prime, x).degree() <= 0:
                neg_q = False
            else:
                r = roots(f_expr, x)
                # Ensure we can find all roots of f(x) to construct K
                if sum(r.values()) == f.degree():
                    K_ext = list(r.keys())
                    K_irr = [e for e in K_ext if not (e.is_rational is True)]
                    
                    if not K_irr:
                        # K is just Q, so we factor f'(x) over Q
                        factors = factor_list(f_prime)
                        is_sub = all(Poly(fac, x).degree() == 1 for fac, _ in factors[1])
                    else:
                        # K is a non-trivial extension, find a primitive element
                        if len(K_irr) == 1:
                            K_prim = K_irr[0]
                        else:
                            K_prim, _ = primitive_element(K_irr, ex=True, polys=False)
                        
                        # Factor f'(x) over K
                        factors = factor_list(f_prime, extension=K_prim)
                        is_sub = all(Poly(fac, x).degree() == 1 for fac, _ in factors[1])
                    
                    # The conclusion is that L is a subfield of K.
                    # We want the negation of the conclusion.
                    neg_q = not is_sub
        except Exception:
            neg_q = False

    return [h1, h2, h3, neg_q]
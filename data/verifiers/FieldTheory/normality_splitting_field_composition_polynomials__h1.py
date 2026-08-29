import sympy
import sympy.polys.numberfields
from sympy.abc import x

# Top-level setup
# (No specific named objects needed for this FieldTheory conjecture)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (f, g) of sympy expressions in x.
    We assume the base field K is Q.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f, g = witness
        else:
            return [False, False]
            
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        
        # H1: f and g are valid expressions that can be interpreted as polynomials in x
        f_poly = sympy.Poly(f, x)
        g_poly = sympy.Poly(g, x)
        H1 = True
    except Exception:
        return [False, False]

    try:
        # Find the roots of P(x) = f(g(x))
        # We solve f(y) = 0, then g(x) = y to find exact algebraic roots
        y_roots = sympy.solve(f, x)
        P_roots = []
        for y in y_roots:
            x_roots = sympy.solve(g - y, x)
            P_roots.extend(x_roots)
            
        unique_roots = list(set(P_roots))
        
        if not unique_roots:
            neg_Q = False
        else:
            # Compute the primitive element of the splitting field L over Q
            M_theta, coeffs = sympy.polys.numberfields.primitive_element(unique_roots, x)
            theta = sum(c * r for c, r in zip(coeffs, unique_roots))
            
            # Fast path for real fields:
            # If all roots are real, L is a subfield of R.
            # If the minimal polynomial of the primitive element has any complex roots,
            # then M_theta does not split completely in L, so L is not normal.
            try:
                all_real = all(r.is_real for r in unique_roots)
                if all_real:
                    num_roots = sympy.nroots(M_theta)
                    has_complex = any(abs(sympy.im(nr)) > 1e-9 for nr in num_roots)
                    if has_complex:
                        return [H1, True]
            except Exception:
                pass
                
            # Fallback to exact algebraic factorization:
            # L is normal over Q iff M_theta splits completely into linear factors in L = Q(theta)
            factors = sympy.factor_list(M_theta, extension=theta)[1]
            is_normal = all(sympy.degree(fac, x) == 1 for fac, mult in factors)
            neg_Q = not is_normal
            
    except Exception:
        neg_Q = False
        
    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: L is the splitting field of the composite polynomial f(g(x)) over K",
    "¬Q: L is not a normal extension of K"
]

N_HYP = 1
NEG_Q_INDEX = 1
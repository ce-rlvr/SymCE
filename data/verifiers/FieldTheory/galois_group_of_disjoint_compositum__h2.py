import sympy
from sympy import Rational, Integer, I, pi, exp, cbrt, sqrt, CRootOf, AlgebraicNumber
from sympy import minpoly, gcd, divisors, degree, Poly, factor
from sympy.abc import x
from sympy.polys.numberfields import primitive_element

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If K and L are extensions of F contained in a common extension, and K \cap L = F,
    then Gal(KL/F) is isomorphic to Gal(K/F) x Gal(L/F)."
    
    The witness should be a tuple of two algebraic numbers (a, b) generating K and L over Q.
    """
    try:
        a, b = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: F is a field. We use F = Q, which is a field.
    h1 = True
    
    # H2: K and L are contained in a common extension field.
    # Since a and b are algebraic numbers, they are both contained in C.
    h2 = True
    
    # H3: K \cap L = F
    try:
        p_a = minpoly(a, x)
        p_b = minpoly(b, x)
        d1 = degree(p_a, x)
        d2 = degree(p_b, x)
        
        # Compute the degree of the compositum KL = Q(a, b)
        elem, _ = primitive_element([a, b], x)
        p_ab = minpoly(elem, x)
        d12 = degree(p_ab, x)
        
        # The intersection degree [K \cap L : Q] must divide gcd(d1, d2)
        # and is bounded above by (d1 * d2) / d12.
        g = gcd(d1, d2)
        max_d_int = (d1 * d2) / d12
        possible_d_ints = [d for d in divisors(g) if d <= max_d_int]
        
        # If the only possible intersection degree is 1, then K \cap L = Q.
        h3 = (possible_d_ints == [1])
    except Exception:
        h3 = False
        
    # ¬Q: Gal(KL/F) is NOT isomorphic to Gal(K/F) x Gal(L/F)
    try:
        def aut_size(gen, poly_expr):
            # Attempt to use field_isomorphism to count roots in the generated field
            try:
                from sympy.polys.numberfields import field_isomorphism
                poly_obj = Poly(poly_expr, x)
                roots = poly_obj.all_roots()
                count = 0
                for r in roots:
                    if field_isomorphism(r, gen) is not None:
                        count += 1
                return count
            except Exception:
                pass
                
            # Fallback: factor the minimal polynomial over the extension field
            factored = factor(poly_expr, extension=gen)
            if factored.is_Mul:
                factors = factored.args
            else:
                factors = [factored]
            
            count = 0
            for f in factors:
                if f.is_Pow:
                    base = f.base
                    exp_val = f.exp
                else:
                    base = f
                    exp_val = 1
                
                if degree(base, x) == 1:
                    count += exp_val
                    
            if count == 0:
                raise ValueError("Automorphism group size cannot be 0")
            return count

        size_K = aut_size(a, p_a)
        size_L = aut_size(b, p_b)
        size_KL = aut_size(elem, p_ab)
        
        # If the sizes of the groups differ, they cannot be isomorphic.
        neg_q = (size_KL != size_K * size_L)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K and L are contained in a common extension field",
    "H_3: K \\cap L = F",
    "¬Q: Gal(KL/F) is not isomorphic to Gal(K/F) x Gal(L/F)"
]

N_HYP = 3
NEG_Q_INDEX = 3
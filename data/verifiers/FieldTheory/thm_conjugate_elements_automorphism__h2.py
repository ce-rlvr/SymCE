import sympy
from sympy import minpoly, factor, Poly, solve, simplify, AlgebraicNumber, I, sqrt, Rational, pi, exp
from sympy.abc import x
from sympy.polys.numberfields import to_number_field

# Top-level setup
Q = sympy.QQ

def conditions(witness) -> list[bool]:
    """
    Given a witness (K_gen, alpha, beta) where K = Q(K_gen) and F = Q,
    checks if it is a valid counterexample to the false conjecture.
    """
    try:
        K_gen, alpha, beta = witness
    except Exception:
        return [False, False]
        
    # H_1: K/F is a normal extension
    try:
        p_K = minpoly(K_gen, x)
        # Factor the minimal polynomial of K_gen over K = Q(K_gen)
        factored = factor(p_K, extension=K_gen)
        factors = factored.args if factored.is_Mul else [factored]
        
        is_normal = True
        roots_K = []
        for f in factors:
            if f.has(x):
                # If any irreducible factor has degree > 1, it doesn't split completely in K
                if Poly(f, x).degree() != 1:
                    is_normal = False
                else:
                    # Collect the roots that are in K (these correspond to automorphisms of K/Q)
                    r = solve(f, x)
                    if r:
                        roots_K.append(r[0])
    except Exception:
        is_normal = False
        roots_K = []

    # Conclusion: alpha and beta share the same minimal polynomial over F
    # iff there exists sigma in Aut(K/F) such that sigma(alpha) = beta
    try:
        p_alpha = minpoly(alpha, x)
        p_beta = minpoly(beta, x)
        lhs = (p_alpha == p_beta)
    except Exception:
        lhs = False

    try:
        def get_poly_in_K(val, generator):
            """Expresses val as a polynomial in the generator of K, if val is in K."""
            try:
                alg_num = to_number_field(val, generator)
                if isinstance(alg_num, AlgebraicNumber):
                    coeffs = alg_num.coeffs()
                    poly_expr = sum(c * x**(len(coeffs) - 1 - i) for i, c in enumerate(coeffs))
                    return poly_expr
                else:
                    # If it's a rational number, it's just a constant polynomial
                    return alg_num * x**0
            except Exception:
                return None

        g_alpha = get_poly_in_K(alpha, K_gen)
        g_beta = get_poly_in_K(beta, K_gen)
        
        # If either alpha or beta is not in K, no automorphism of K can map alpha to beta
        if g_alpha is None or g_beta is None:
            rhs = False
        else:
            rhs = False
            # Apply each automorphism sigma in Aut(K/Q) to alpha
            for r in roots_K:
                mapped_alpha = g_alpha.subs(x, r)
                diff = mapped_alpha - beta
                
                if diff == 0:
                    rhs = True
                    break
                try:
                    # minpoly(diff) == x iff diff == 0
                    if minpoly(diff, x) == x:
                        rhs = True
                        break
                except Exception:
                    if simplify(diff) == 0:
                        rhs = True
                        break
    except Exception:
        rhs = False

    try:
        iff_condition = (lhs == rhs)
        neg_Q = not iff_condition
    except Exception:
        neg_Q = False

    return [is_normal, neg_Q]

CONDITION_LABELS = [
    "H_1: K/F is a normal extension",
    "¬Q: The equivalence between sharing a minimal polynomial and being mapped by an automorphism fails"
]

N_HYP = 1
NEG_Q_INDEX = 1
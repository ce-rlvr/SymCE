import sympy
from sympy import minpoly, degree, Symbol

CONDITION_LABELS = [
    "H_1: α and β are algebraic over F",
    "H_2: The simple extension F(α) is a subfield of F(β)",
    "¬Q: F(α) = F(β) iff deg(minpoly(α, F)) = deg(minpoly(β, F)) is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (F, alpha, beta) or an object with
    the necessary attributes/methods to evaluate the field extensions.
    """
    # Default to False
    h1_ok = False
    h2_ok = False
    neg_q_ok = False

    try:
        # If the witness is a custom object with pre-computed properties
        if hasattr(witness, 'is_algebraic_alpha') and hasattr(witness, 'is_algebraic_beta'):
            h1_ok = bool(witness.is_algebraic_alpha and witness.is_algebraic_beta)
            h2_ok = bool(witness.F_alpha_is_subfield_F_beta)
            
            F_alpha_eq_F_beta = bool(witness.F_alpha_eq_F_beta)
            deg_eq = bool(witness.deg_alpha == witness.deg_beta)
            
            # Conclusion is the equivalence: F(α) = F(β) <==> deg(α) = deg(β)
            # We want the negation of the conclusion
            neg_q_ok = not (F_alpha_eq_F_beta == deg_eq)
            
            return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        pass

    try:
        # If the witness is a tuple (F, alpha, beta)
        if isinstance(witness, tuple) and len(witness) == 3:
            F, alpha, beta = witness
            
            x = Symbol('x')
            
            # H1: alpha and beta are algebraic over F
            try:
                poly_alpha = minpoly(alpha, x, domain=F)
                poly_beta = minpoly(beta, x, domain=F)
                h1_ok = True
            except Exception:
                h1_ok = False

            # H2: F(alpha) is a subfield of F(beta)
            # In sympy, we can check if alpha is in F(beta) by checking if it can be 
            # expressed as a polynomial in beta with coefficients in F.
            # For simplicity in evaluation, we might rely on sympy's algebraic field methods
            try:
                if h1_ok:
                    # Create the extension fields
                    F_beta = sympy.QQ.algebraic_field(beta) if F == sympy.QQ else F.algebraic_field(beta)
                    F_alpha = sympy.QQ.algebraic_field(alpha) if F == sympy.QQ else F.algebraic_field(alpha)
                    
                    # Check if alpha is in F(beta)
                    h2_ok = F_beta.of_type(alpha) or alpha in F_beta
            except Exception:
                # Fallback for subfield check if algebraic_field fails
                try:
                    h2_ok = bool(alpha == beta or sympy.simplify(alpha - beta) == 0 or 
                                 (poly_beta.subs(x, alpha) == 0))
                except Exception:
                    h2_ok = False

            # Conclusion: F(alpha) == F(beta) iff deg(poly_alpha) == deg(poly_beta)
            try:
                if h1_ok:
                    deg_alpha = degree(poly_alpha, x)
                    deg_beta = degree(poly_beta, x)
                    deg_eq = (deg_alpha == deg_beta)
                    
                    # Check if F(beta) is a subfield of F(alpha) to establish equality
                    try:
                        F_alpha_eq_F_beta = h2_ok and (F_alpha.of_type(beta) or beta in F_alpha)
                    except Exception:
                        F_alpha_eq_F_beta = h2_ok and deg_eq  # Fallback logic for standard fields
                    
                    neg_q_ok = not (F_alpha_eq_F_beta == deg_eq)
            except Exception:
                neg_q_ok = False

    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]
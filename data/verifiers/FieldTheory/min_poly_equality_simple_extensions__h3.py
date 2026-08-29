import sympy
from sympy import QQ, Symbol, minpoly, sqrt, I, Rational

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Given a witness tuple (F, alpha, beta), checks if it is a valid counterexample.
    """
    try:
        F, alpha, beta = witness
    except Exception:
        return [False, False, False]
        
    # H1: F is a field
    try:
        h1 = (F == QQ) or getattr(F, 'is_Field', False) or getattr(F, 'is_field', False)
    except Exception:
        h1 = False
        
    # H2: alpha and beta are algebraic over F
    try:
        p_a = minpoly(alpha, x, domain=F)
        p_b = minpoly(beta, x, domain=F)
        h2 = p_a.degree() > 0 and p_b.degree() > 0
    except Exception:
        h2 = False
        
    # Negated Conclusion: 
    # F(α) = F(β) is NOT equivalent to deg(minpoly(α, F)) == deg(minpoly(β, F))
    try:
        d_a = minpoly(alpha, x, domain=F).degree()
        d_b = minpoly(beta, x, domain=F).degree()
        
        # Compute the degree of the composite field F(α, β) over F.
        # By the primitive element theorem, α + c*β generates F(α, β) for almost all c.
        d_ab = 0
        for c in range(1, 6):
            deg = minpoly(alpha + c * beta, x, domain=F).degree()
            if deg > d_ab:
                d_ab = deg
            # Break early if we hit the maximum possible degree
            if d_ab == d_a * d_b:
                break
                
        # F(α) == F(β) if and only if F(α, β) has the same degree over F as α and β.
        fields_equal = (d_ab == d_a and d_a == d_b)
        degrees_equal = (d_a == d_b)
        
        neg_q = (fields_equal != degrees_equal)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: α and β are algebraic over F",
    "¬Q: F(α) = F(β) is not equivalent to deg(minpoly(α, F)) == deg(minpoly(β, F))"
]

N_HYP = 2
NEG_Q_INDEX = 2
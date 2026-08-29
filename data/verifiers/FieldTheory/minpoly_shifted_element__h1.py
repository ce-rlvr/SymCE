import sympy
from sympy import minpoly, Poly, degree, Rational

# Top-level setup for potential witness expressions
x = sympy.Symbol('x')

def conditions(witness):
    try:
        alpha = witness.get('alpha')
        m = witness.get('m')
        c = witness.get('c')
        x_sym = witness.get('x')
        
        if any(v is None for v in [alpha, m, c, x_sym]):
            return [False, False, False]
            
        m_expr = m.as_expr() if isinstance(m, Poly) else m
        
        # H_1: alpha is algebraic over F with minimal polynomial m(x)
        # We use F = Q as the base field for verification.
        try:
            mp_alpha = minpoly(alpha, x_sym)
            is_algebraic = True
        except Exception:
            is_algebraic = False
            
        try:
            p = Poly(m_expr, x_sym)
            is_monic = (p.LC() == 1)
            is_root = (m_expr.subs(x_sym, alpha).simplify() == 0)
            
            # Check if m(x) is irreducible over its coefficient field.
            # Degree 1 polynomials are trivially irreducible.
            if degree(m_expr, x_sym) == 1:
                is_irreducible = True
            else:
                # If coefficients are rational, check irreducibility over Q
                if all(coef.is_Rational == True for coef in p.coeffs()):
                    from sympy import factor_list
                    factors = factor_list(m_expr)[1]
                    is_irreducible = (len(factors) == 1 and factors[0][1] == 1)
                else:
                    is_irreducible = False
        except Exception:
            is_monic = False
            is_root = False
            is_irreducible = False
            
        h1_ok = is_algebraic and is_monic and is_root and is_irreducible
    except Exception:
        h1_ok = False
        
    try:
        # H_2: c is an element of the base field F
        # Since we use F = Q, c must be a rational number.
        h2_ok = (sympy.sympify(c).is_Rational == True)
    except Exception:
        h2_ok = False
        
    try:
        # ¬Q: The minimal polynomial of alpha + c over F is not m(x - c)
        # The conjecture fails because m(x) might be the minimal polynomial over an extension field E,
        # rather than over the base field F, which was dropped from the hypotheses.
        mp_alpha_c = minpoly(alpha + c, x_sym)
        m_shifted = m_expr.subs(x_sym, x_sym - c)
        
        diff = sympy.expand(mp_alpha_c - m_shifted)
        neg_q_ok = (diff != 0)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: alpha is algebraic over F with minimal polynomial m(x)",
    "H_2: c is an element of the base field F",
    "¬Q: The minimal polynomial of alpha + c over F is not m(x - c)"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x
from sympy import minpoly, Poly

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    F = sympy.QQ
    alpha = None
    beta = None
    
    # Extract F, alpha, beta from the witness
    try:
        if isinstance(witness, dict):
            F = witness.get('F', sympy.QQ)
            alpha = witness.get('alpha')
            beta = witness.get('beta')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                F, alpha, beta = witness
            elif len(witness) == 2:
                alpha, beta = witness
            elif len(witness) == 1:
                alpha = beta = witness[0]
        elif hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            alpha = beta = witness
        else:
            F = getattr(witness, 'F', sympy.QQ)
            alpha = getattr(witness, 'alpha', None)
            beta = getattr(witness, 'beta', None)
    except Exception:
        pass

    if alpha is None or beta is None:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        h1 = bool(getattr(F, 'is_Field', False) or getattr(F, 'is_field', False))
    except Exception:
        h1 = False

    # H_2: \alpha \in K and \beta \in L are algebraic over F
    try:
        mp_alpha_expr = minpoly(alpha, x)
        mp_beta_expr = minpoly(beta, x)
        
        mp_alpha = Poly(mp_alpha_expr, x, domain=F)
        mp_beta = Poly(mp_beta_expr, x, domain=F)
        
        h2 = bool(mp_alpha.degree() > 0 and mp_beta.degree() > 0)
    except Exception:
        h2 = False

    # H_3: \alpha and \beta have the same minimal polynomial over F
    try:
        mp_alpha_monic = mp_alpha.monic()
        mp_beta_monic = mp_beta.monic()
        h3 = bool(mp_alpha_monic == mp_beta_monic)
    except Exception:
        h3 = False

    # ¬Q: There does NOT exist an F-isomorphism from the simple extension F(\alpha) to F(\beta) mapping \alpha to \beta.
    # If the minimal polynomial is reducible, F[\alpha] has zero divisors and is not a domain.
    # Thus, the field of fractions F(\alpha) does not exist (it is not a field), 
    # so it cannot be a simple field extension isomorphic to F(\beta).
    try:
        neg_q = not bool(mp_alpha_monic.is_irreducible)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha and beta are algebraic over F",
    "H_3: alpha and beta have the same minimal polynomial over F",
    "¬Q: F(alpha) and F(beta) are not isomorphic simple field extensions"
]

N_HYP = 3
NEG_Q_INDEX = 3
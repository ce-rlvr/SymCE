import sympy as sp

# Top-level setup
# We define standard symbols and domains that might be used in the witness.
x = sp.Symbol('x')
QQ = sp.QQ

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    
    The witness should be a dictionary containing:
      - 'alpha': an algebraic number
      - 'beta': an algebraic number
      - 'm': a SymPy expression representing m(x)
      - 'x': the SymPy symbol used in m(x)
      - 'F': (optional) the SymPy domain for the field F, defaults to QQ
    """
    try:
        alpha = witness['alpha']
        beta = witness['beta']
        m = witness['m']
        sym_x = witness['x']
        F = witness.get('F', sp.QQ)
    except (KeyError, TypeError):
        return [False, False, False, False]

    # H1: m(x) is the minimal polynomial of alpha over F
    # We check if m(alpha) == 0 and m(x) is irreducible over F.
    # (The dropped hypothesis in the conjecture is likely that m(x) must be monic).
    try:
        m_poly = sp.Poly(m, sym_x, domain=F)
        # Check root condition
        root_check = sp.simplify(m.subs(sym_x, alpha)) == 0
        # Check irreducibility
        irreducible_check = m_poly.is_irreducible
        h1 = bool(root_check and irreducible_check)
    except Exception:
        h1 = False

    # H2: beta^2 = alpha
    try:
        h2 = bool(sp.simplify(beta**2 - alpha) == 0)
    except Exception:
        h2 = False

    # H3: beta is not an element of F(alpha)
    # We verify this by checking that the degree of the minimal polynomial of beta over F
    # is strictly greater than the degree of the minimal polynomial of alpha over F.
    # Since beta^2 = alpha, beta not in F(alpha) implies [F(beta) : F] = 2 * [F(alpha) : F].
    try:
        minpoly_alpha = sp.minpoly(alpha, sym_x, domain=F)
        minpoly_beta = sp.minpoly(beta, sym_x, domain=F)
        deg_alpha = sp.degree(minpoly_alpha, sym_x)
        deg_beta = sp.degree(minpoly_beta, sym_x)
        h3 = bool(deg_beta > deg_alpha)
    except Exception:
        h3 = False

    # ¬Q: The minimal polynomial of beta over F is NOT m(x^2)
    try:
        # We compute the true minimal polynomial of beta over F (which is always monic)
        true_minpoly_beta = sp.minpoly(beta, sym_x, domain=F)
        
        # The conjecture claims it should be exactly m(x^2)
        m_x2 = m.subs(sym_x, sym_x**2)
        
        # The conclusion fails if they are not identical polynomials
        poly_diff = sp.simplify(true_minpoly_beta - m_x2)
        neg_q = bool(poly_diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m(x) is the minimal polynomial of alpha over F",
    "H_2: beta^2 = alpha",
    "H_3: beta is not an element of F(alpha)",
    "¬Q: The minimal polynomial of beta over F is NOT m(x^2)"
]

N_HYP = 3
NEG_Q_INDEX = 3
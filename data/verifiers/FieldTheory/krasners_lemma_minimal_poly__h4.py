import sympy

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and negated conclusion for the false conjecture 
    related to Krasner's Lemma.
    
    The witness is expected to be a dictionary with:
      - 'alpha': a sympy algebraic expression
      - 'beta': a sympy algebraic expression
      - 'r': a positive number (distance bound)
      - 'abs_val': string, expected to be 'trivial' for this verifier
    Alternatively, a tuple (alpha, beta, r) is accepted, assuming the trivial absolute value.
    """
    try:
        if isinstance(witness, dict):
            alpha = witness['alpha']
            beta = witness['beta']
            r = float(witness['r'])
            abs_val = witness.get('abs_val', 'trivial')
        else:
            alpha, beta, r = witness[:3]
            r = float(r)
            abs_val = 'trivial'
    except Exception:
        return [False] * 5

    # H_1: K is a field complete with respect to a non-archimedean absolute value
    # We use K = Q with the trivial absolute value, which is non-archimedean and complete.
    try:
        h1 = (abs_val == 'trivial')
    except Exception:
        h1 = False

    # H_2: α and β are separable algebraic elements over K
    # In characteristic 0 (like Q), all algebraic elements are separable.
    # We verify they are algebraic by successfully computing their minimal polynomials.
    try:
        m_a = sympy.minpoly(alpha, x)
        m_b = sympy.minpoly(beta, x)
        h2 = True
    except Exception:
        h2 = False

    # H_3: m_α(x) is the minimal polynomial of α over K
    # This is a definitional hypothesis in our setup.
    h3 = True

    # H_4: Assume the distance between α and β is strictly less than r
    # Under the trivial absolute value, distance is 0 if equal, 1 if distinct.
    try:
        if alpha == beta or sympy.simplify(alpha - beta) == 0:
            dist = 0.0
        else:
            dist = 1.0
        h4 = bool(dist < r)
    except Exception:
        h4 = False

    # ¬Q: The minimal polynomial of α over K(β) is NOT exactly x - α
    # This is equivalent to saying α is NOT in K(β).
    # We check this by verifying if the degree of Q(α, β) over Q is strictly greater than Q(β) over Q.
    try:
        deg_beta = sympy.minpoly(beta, x).degree()
        # By the primitive element theorem, Q(α, β) = Q(α + c*β) for almost all integers c.
        deg_ext = max(sympy.minpoly(alpha + c * beta, x).degree() for c in range(1, 6))
        neg_q = bool(deg_ext > deg_beta)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field complete with respect to a non-archimedean absolute value",
    "H_2: α and β are separable algebraic elements over K",
    "H_3: m_α(x) is the minimal polynomial of α over K",
    "H_4: The distance between α and β is strictly less than r",
    "¬Q: α is not in K(β) (minimal polynomial is not x - α)"
]

N_HYP = 4
NEG_Q_INDEX = 4
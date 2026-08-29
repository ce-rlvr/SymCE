import sympy
from sympy import Symbol, minpoly, degree, sqf_list

# Top-level setup
QQ = sympy.QQ
x = Symbol('x')

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture related to Krasner's Lemma.
    """
    # Extract witness components
    if isinstance(witness, dict):
        K = witness.get('K', QQ)
        K_bar = witness.get('K_bar', 'QQ_bar')
        alpha = witness.get('alpha', None)
        beta = witness.get('beta', None)
    elif isinstance(witness, tuple):
        if len(witness) == 4:
            K, K_bar, alpha, beta = witness
        elif len(witness) == 2:
            K, K_bar = QQ, 'QQ_bar'
            alpha, beta = witness
        else:
            return [False, False, False, False]
    else:
        return [False, False, False, False]

    # H_1: K is a field complete with respect to a non-archimedean absolute value
    # (Note: Any field is complete with respect to the trivial absolute value, which is non-archimedean)
    try:
        if K == QQ:
            h1 = True
        elif hasattr(K, 'is_Field') and K.is_Field:
            h1 = True
        elif isinstance(K, str) and K in ['Qp', 'Q_p', 'Fp((t))', 'C_p']:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: K_bar is an algebraic closure of K
    try:
        if K_bar is not None:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: alpha in K_bar is separable over K
    try:
        p_alpha = minpoly(alpha, x)
        factors = sqf_list(p_alpha)[1]
        # Separable iff the minimal polynomial is square-free
        h3 = all(mult == 1 for factor, mult in factors)
    except Exception:
        h3 = False

    # ¬Q: K(alpha) is not contained in K(beta)
    try:
        p_beta = minpoly(beta, x)
        deg_beta = degree(p_beta, x)
        
        neg_q = False
        # If K(alpha) is contained in K(beta), then K(alpha, beta) = K(beta).
        # We check if the degree of K(alpha, beta) over K is strictly greater than the degree of K(beta).
        # We use alpha + c * beta as a candidate for the primitive element of K(alpha, beta).
        for c in [1, 2, 3, 4, 5]:
            p_ab = minpoly(alpha + c * beta, x)
            deg_ab = degree(p_ab, x)
            if deg_ab > deg_beta:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field complete with respect to a non-archimedean absolute value",
    "H_2: K_bar is an algebraic closure of K",
    "H_3: alpha in K_bar is separable over K",
    "¬Q: K(alpha) is not contained in K(beta)"
]

N_HYP = 3
NEG_Q_INDEX = 3
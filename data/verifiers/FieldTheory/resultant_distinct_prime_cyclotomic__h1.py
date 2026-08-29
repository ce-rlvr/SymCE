import sympy

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (p, q) or a dict {'p': p, 'q': q} representing the indices.
    """
    try:
        if isinstance(witness, dict):
            p = witness['p']
            q = witness['q']
        else:
            p, q = witness
        # p and q must be valid indices for cyclotomic polynomials (positive integers)
        h1 = isinstance(p, (int, sympy.Integer)) and isinstance(q, (int, sympy.Integer)) and p >= 1 and q >= 1
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            poly_p = sympy.cyclotomic_poly(p, x)
            poly_q = sympy.cyclotomic_poly(q, x)
            res = sympy.resultant(poly_p, poly_q, x)
            # The conclusion is that the resultant is 1.
            # We want the negated conclusion: the resultant is NOT 1.
            neg_q = bool(res != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are positive integers",
    "¬Q: Res(Phi_p, Phi_q) != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
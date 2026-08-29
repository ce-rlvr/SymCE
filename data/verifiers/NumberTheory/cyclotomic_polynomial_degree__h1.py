import sympy

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is likely that n >= 1.
    """
    try:
        n = witness
        # H_1: Phi_n(x) is the n-th cyclotomic polynomial
        # This implies n is an integer index for the polynomial.
        h1 = isinstance(n, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        # Evaluate the conclusion: The degree of Phi_n(x) is phi(n)
        poly = sympy.cyclotomic_poly(n, x)
        deg = sympy.degree(poly, x)
        tot = sympy.totient(n)
        q = (deg == tot)
    except Exception:
        # If cyclotomic_poly is undefined (e.g., for n <= 0), the conclusion fails.
        q = False

    neg_q = not q

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Phi_n(x) is the n-th cyclotomic polynomial",
    "¬Q: The degree of Phi_n(x) is not phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1
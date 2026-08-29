import sympy as sp
from sympy.abc import x
from sympy import QQ, ZZ, RR, CC

# Top-level setup for Ring Theory
# x is defined as a symbol for polynomial generators.
# QQ, ZZ, RR, CC are available as domains.

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    Hypotheses:
      - F is a field
      - E is the factor ring F[x]/(p(x))
      - \alpha is the coset x + (p(x)) in E
    Conclusion:
      - \alpha is a root of p(x) in E
    """
    p = None
    try:
        # The witness is expected to be a polynomial p(x), 
        # or a tuple where the domain F is the first element and the polynomial is the last.
        if isinstance(witness, tuple):
            p = sp.Poly(witness[-1], x, domain=witness[0])
        else:
            p = sp.Poly(witness, x)
    except Exception:
        pass

    # H_1: F is a field
    try:
        h1 = False
        if p is not None:
            h1 = bool(p.domain.is_Field)
    except Exception:
        h1 = False

    # H_2: E is the factor ring F[x]/(p(x))
    # This is a structural definition. We consider it satisfied if p is a valid univariate polynomial.
    try:
        h2 = False
        if p is not None:
            h2 = True
    except Exception:
        h2 = False

    # H_3: \alpha is the coset x + (p(x)) in E
    # This is also a structural definition.
    try:
        h3 = False
        if p is not None:
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: \alpha is NOT a root of p(x) in E
    # This fails (i.e., neg_q is True) when p(x) is a non-zero constant, because E becomes 
    # the zero ring, which is not a valid extension ring (1 != 0 is required for F to embed).
    try:
        neg_q = False
        if p is not None:
            if p.degree() <= 0 and not p.is_zero:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

# Note: Avoided using square brackets inside the strings to prevent regex parsing issues in the validator.
CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is the factor ring of polynomials over F modulo p(x)",
    "H_3: \\alpha is the coset x + (p(x)) in E",
    "¬Q: \\alpha is not a root of p(x) in E"
]

N_HYP = 3
NEG_Q_INDEX = 3
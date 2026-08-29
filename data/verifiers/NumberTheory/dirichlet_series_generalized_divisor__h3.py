import sympy as sp

# Top-level setup
# (No specific named objects required for this number theory conjecture, 
# but we provide standard ones as requested)
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    Hypotheses:
      - a is a complex number
      - s is a complex number
      - Re(s) > 1 + Re(a)
    Conclusion:
      - Sum_{n=1}^infty sigma_a(n)/n^s = zeta(s)*zeta(s-a)
    """
    try:
        a, s = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: a is a complex number
    try:
        a_sym = sp.sympify(a)
        h1 = bool(a_sym.is_number and a_sym.is_finite)
    except Exception:
        h1 = False

    # H_2: s is a complex number
    try:
        s_sym = sp.sympify(s)
        h2 = bool(s_sym.is_number and s_sym.is_finite)
    except Exception:
        h2 = False

    # H_3: Re(s) > 1 + Re(a)
    try:
        h3 = bool(sp.re(s_sym) > 1 + sp.re(a_sym))
    except Exception:
        h3 = False

    # neg_Q: Conclusion fails
    # The conclusion is that the Dirichlet series converges and equals zeta(s)zeta(s-a).
    # Mathematically, this series converges absolutely and equals the RHS 
    # if and only if Re(s) > 1 and Re(s) > 1 + Re(a).
    # If it diverges (which happens when Re(s) <= 1), the equality to the finite RHS fails.
    try:
        # Check if the series converges
        converges = bool(sp.re(s_sym) > 1) and bool(sp.re(s_sym) > 1 + sp.re(a_sym))
        
        # The conclusion holds iff the series converges
        q = converges
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a is a complex number",
    "H_2: s is a complex number",
    "H_3: Re(s) > 1 + Re(a)",
    "¬Q: \\sum_{n=1}^\\infty \\frac{\\sigma_a(n)}{n^s} \\neq \\zeta(s)\\zeta(s-a)"
]

N_HYP = 3
NEG_Q_INDEX = 3
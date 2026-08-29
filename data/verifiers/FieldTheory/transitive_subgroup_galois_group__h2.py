import sympy

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    """
    Check the hypotheses and negated conclusion for the Transitive Subgroup Theorem.
    The witness is expected to be a polynomial f(x) over a field F (e.g., QQ).
    """
    def get_poly(w):
        if isinstance(w, tuple):
            w = w[0]
        if hasattr(w, 'free_symbols') and w.free_symbols:
            sym = list(w.free_symbols)[0]
        else:
            sym = x
        return sympy.Poly(w, sym)

    # H_1: F is a field.
    # We assume the coefficients of the polynomial implicitly define the field F 
    # (e.g., QQ if given integer/rational coefficients).
    try:
        poly = get_poly(witness)
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: f(x) is a separable polynomial.
    # A polynomial is separable iff it is coprime to its formal derivative.
    try:
        poly = get_poly(witness)
        deriv = poly.diff()
        gcd_poly = poly.gcd(deriv)
        h2_ok = gcd_poly.degree() == 0
    except Exception:
        h2_ok = False

    # H_3: The degree of f(x) is n.
    # This establishes n >= 1 for the Galois group to act on its roots.
    try:
        poly = get_poly(witness)
        h3_ok = poly.degree() >= 1
    except Exception:
        h3_ok = False

    # H_4: K is the splitting field of f(x) over F.
    # This is a definitional hypothesis for K.
    try:
        poly = get_poly(witness)
        h4_ok = True
    except Exception:
        h4_ok = False

    # ¬Q: Gal(K/F) does NOT act transitively on the roots of f(x).
    # For a separable polynomial, the Galois group acts transitively on the roots 
    # if and only if the polynomial is irreducible over F.
    # Thus, the conclusion fails (¬Q is True) iff f(x) is reducible over F.
    try:
        poly = get_poly(witness)
        factors = poly.factor_list()
        # factors[1] contains tuples of (irreducible_factor, multiplicity)
        # It is reducible if the sum of multiplicities of non-constant factors is > 1
        neg_q_ok = sum(mult for _, mult in factors[1]) > 1
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a separable polynomial",
    "H_3: The degree of f(x) is n",
    "H_4: K is the splitting field of f(x) over F",
    "¬Q: Gal(K/F) does not act transitively on the roots of f(x) (f is reducible)"
]

N_HYP = 4
NEG_Q_INDEX = 4
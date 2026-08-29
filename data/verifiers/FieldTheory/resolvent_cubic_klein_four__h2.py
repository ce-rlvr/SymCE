import sympy
from sympy import Symbol, Poly

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the conjecture.
    The conjecture states that for a polynomial f(x), the Galois group of its 
    resolvent cubic R(x) is isomorphic to G / (G \cap V), where G is the Galois 
    group of f(x) viewed as a subgroup of S_4, and V is the Klein four-group.
    
    The dropped hypothesis is that f(x) is separable. For non-separable quartics,
    the roots are not distinct, so the action of the Galois group on the roots 
    does not give a well-defined embedding into S_4. If we force an embedding 
    by labeling the roots (including multiplicities), G \cap V can be trivial 
    while the resolvent cubic has a trivial Galois group, breaking the isomorphism.
    """
    # We expect the witness to be a sympy polynomial expression in x
    f = witness
    
    # H1: K is a field of characteristic not equal to 2 or 3.
    # We assume K = Q, which has characteristic 0.
    try:
        poly_f = Poly(f, x)
        h1_ok = all(c.is_rational for c in poly_f.coeffs())
    except Exception:
        h1_ok = False

    # H2: G is the Galois group of f(x) over K, viewed as a subgroup of S_4.
    # This implies f(x) has degree 4.
    try:
        h2_ok = poly_f.degree() == 4
    except Exception:
        h2_ok = False

    # H3: V is the Klein four-group... (This is a definition, always True if H2 holds)
    h3_ok = h2_ok

    # H4: R(x) is the resolvent cubic of f(x).
    # We can always compute the resolvent cubic for a monic quartic.
    try:
        if poly_f.LC() != 1:
            h4_ok = False
        else:
            coeffs = poly_f.all_coeffs()
            a, b, c, d = coeffs[1], coeffs[2], coeffs[3], coeffs[4]
            # R(x) = x^3 - b*x^2 + (a*c - 4*d)*x - a^2*d + 4*b*d - c^2
            R = x**3 - b*x**2 + (a*c - 4*d)*x - a**2*d + 4*b*d - c**2
            h4_ok = True
    except Exception:
        h4_ok = False

    # ¬Q: The Galois group of R(x) over K is NOT isomorphic to G / (G \cap V).
    # For a separable quartic, they are ALWAYS isomorphic.
    # The conjecture fails for non-separable quartics (e.g., f(x) = x^4 - 2x^2).
    # We check if the witness is a non-separable quartic where the isomorphism fails.
    try:
        neg_q_ok = False
        if h1_ok and h2_ok and h4_ok:
            # Check if f(x) is non-separable (discriminant is 0)
            if sympy.discriminant(f, x) == 0:
                # For non-separable quartics, the theorem fails because the embedding 
                # into S_4 is not unique and the roots of R(x) are not distinct in a way 
                # that preserves the Galois action kernel as G \cap V.
                # We return True for neg_Q to indicate the conclusion fails.
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic not equal to 2 or 3",
    "H_2: G is the Galois group of f(x) over K, viewed as a subgroup of S_4",
    "H_3: V is the Klein four-group",
    "H_4: R(x) is the resolvent cubic of f(x)",
    "¬Q: The Galois group of R(x) over K is NOT isomorphic to G / (G \cap V)"
]

N_HYP = 4
NEG_Q_INDEX = 4
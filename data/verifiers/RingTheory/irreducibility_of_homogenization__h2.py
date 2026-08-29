import sympy as sp

# Top-level setup
x0, x1, x2, x3, x4, x5 = sp.symbols('x0 x1 x2 x3 x4 x5')

def conditions(witness) -> list[bool]:
    """
    Given a witness (a tuple (f, K) where f is a sympy polynomial in x1..xn and K is a sympy domain),
    returns a list of booleans:
      [H_1_ok, H_2_ok, neg_Q_ok]
    """
    try:
        f, K = witness
    except Exception:
        return [False, False, False]

    # H_1: K is a field
    try:
        h1_ok = K.is_Field
    except Exception:
        h1_ok = False

    # H_2: F is the homogenization of f
    # This is a definitional hypothesis, so it's always True for the constructed F.
    # We will construct F to evaluate the conclusion.
    try:
        if f == 0:
            F = sp.S(0)
        else:
            poly_f = sp.poly(f, domain=K)
            d = poly_f.total_degree()
            # Homogenize f with respect to x0
            # F(x0, x1, ..., xn) = x0^d * f(x1/x0, ..., xn/x0)
            gens = poly_f.gens
            subs_dict = {g: g / x0 for g in gens}
            F_expr = sp.simplify(x0**d * f.subs(subs_dict))
            F = sp.poly(F_expr, *(gens + (x0,)), domain=K)
        h2_ok = True
    except Exception:
        h2_ok = False
        F = None

    # neg_Q: The conclusion FAILS
    # Conclusion: f is irreducible in K[x1..xn] iff F is irreducible in K[x0..xn]
    # So neg_Q is True if (f is irreducible) != (F is irreducible)
    try:
        if F is None:
            neg_q_ok = False
        else:
            # Check irreducibility of f
            if f == 0 or sp.poly(f, domain=K).is_zero:
                f_irred = False
            else:
                f_irred = sp.poly(f, domain=K).is_irreducible

            # Check irreducibility of F
            if F == 0 or F.is_zero:
                F_irred = False
            else:
                F_irred = F.is_irreducible
            
            neg_q_ok = (f_irred != F_irred)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: F is the homogenization of f",
    "¬Q: f is irreducible iff F is irreducible is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2
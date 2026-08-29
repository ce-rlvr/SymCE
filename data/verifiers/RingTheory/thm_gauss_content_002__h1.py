import sympy as sp

# Top-level setup: define symbols that the witness may reference
X, Y, Z, W = sp.symbols('X Y Z W')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness can be a single polynomial f, or a tuple (f, F).
    """
    try:
        if isinstance(witness, tuple):
            f, F_wit = witness
        else:
            f = witness
            d = sp.degree(f, X)
            F_wit = sp.expand(Y**d * f.subs(X, X/Y))
    except Exception:
        return [False, False, False]

    # H_1: f \in R[X] is a non-zero polynomial of degree d
    try:
        if f == 0 or Y in getattr(f, 'free_symbols', set()):
            h1_ok = False
        else:
            p_f = sp.Poly(f, X)
            h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: F \in R[X,Y] is the homogenization of f
    try:
        d = sp.degree(f, X)
        F_expected = sp.expand(Y**d * f.subs(X, X/Y))
        h2_ok = bool(sp.expand(F_wit - F_expected) == 0)
    except Exception:
        h2_ok = False

    # neg_Q: The content of F is NOT equal to the content of f
    try:
        p_f = sp.Poly(f, X)
        domain = p_f.domain
        
        if domain.is_Field:
            # Over a field, the content of any non-zero polynomial is the entire field (ideal <1>).
            # The homogenization will also have content <1>. They are always equal.
            neg_q_ok = False
        else:
            coeffs = p_f.all_coeffs()
            a_d = coeffs[0]
            
            def divides(a, b):
                if a == 0:
                    return b == 0
                q = sp.cancel(b / a)
                try:
                    # Check if the quotient belongs to the base ring
                    domain.from_sympy(q)
                    return True
                except Exception:
                    return False
            
            # The content of F in R[Y][X] is equal to the content of f in R
            # if and only if the leading coefficient a_d divides all coefficients of f.
            ad_divides_all = all(divides(a_d, c) for c in coeffs)
            neg_q_ok = not ad_divides_all
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a non-zero polynomial in X",
    "H_2: F is the homogenization of f",
    "neg_Q: The content of F is NOT equal to the content of f"
]

N_HYP = 2
NEG_Q_INDEX = 2
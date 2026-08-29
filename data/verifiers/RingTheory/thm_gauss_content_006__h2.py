import sympy as sp
from sympy.abc import X, Y, Z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    
    Since content in a UFD is only defined up to multiplication by a unit (associates),
    the strict equality claimed in the conclusion is mathematically false.
    To demonstrate this, the witness must provide a polynomial and valid choices 
    of contents that are not strictly equal.
    
    Expected witness format: a tuple, list, or dict containing:
      - f: the polynomial in ZZ[X, Y]
      - c_Y_f: a valid content of f in Y over ZZ[X]
      - c_X_c_Y_f: a valid content of c_Y_f in X over ZZ
      - c_total: a valid total content of f in X, Y over ZZ
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            c_Y_f = witness.get('c_Y_f')
            c_X_c_Y_f = witness.get('c_X_c_Y_f')
            c_total = witness.get('c_total')
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            f, c_Y_f, c_X_c_Y_f, c_total = witness
        else:
            return [False, False, False]
            
        if any(v is None for v in (f, c_Y_f, c_X_c_Y_f, c_total)):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a Unique Factorization Domain.
    # We are working over R = ZZ, which is a UFD.
    H1 = True

    # H2: c_Y(f) is the content of f viewed as a polynomial in Y over R[X].
    try:
        f_poly_Y = sp.Poly(f, Y, domain='ZZ[X]')
        canonical_c_Y = f_poly_Y.content()
        
        # Check if c_Y_f is an associate of the canonical content in ZZ[X].
        # In ZZ[X], the units are 1 and -1.
        diff1 = sp.expand(c_Y_f - canonical_c_Y)
        diff2 = sp.expand(c_Y_f + canonical_c_Y)
        H2 = bool((diff1 == 0) or (diff2 == 0))
    except Exception:
        H2 = False

    # Conclusion: The content of c_Y(f) as a polynomial in R[X] is equal to the total content of f.
    # We verify that the provided contents are valid, and then check if strict equality FAILS.
    try:
        # Verify that c_X_c_Y_f is a valid content of c_Y_f in X over ZZ
        canonical_c_X = sp.Poly(c_Y_f, X, domain='ZZ').content()
        is_valid_c_X = bool((sp.expand(c_X_c_Y_f - canonical_c_X) == 0) or (sp.expand(c_X_c_Y_f + canonical_c_X) == 0))

        # Verify that c_total is a valid total content of f in X, Y over ZZ
        canonical_c_total = sp.Poly(f, X, Y, domain='ZZ').content()
        is_valid_c_total = bool((sp.expand(c_total - canonical_c_total) == 0) or (sp.expand(c_total + canonical_c_total) == 0))

        if is_valid_c_X and is_valid_c_total:
            # The conjecture claims they are strictly EQUAL.
            # neg_Q is True if they are NOT equal.
            Q = bool(sp.expand(c_X_c_Y_f - c_total) == 0)
            neg_Q = not Q
        else:
            neg_Q = False
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: c_Y(f) is the content of f viewed as a polynomial in Y",
    "¬Q: The content of c_Y(f) is not equal to the total content of f"
]

N_HYP = 2
NEG_Q_INDEX = 2
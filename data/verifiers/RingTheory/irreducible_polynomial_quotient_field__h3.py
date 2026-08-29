import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness is expected to be a polynomial f(x).
    """
    try:
        if isinstance(witness, Poly):
            p = witness
        else:
            p = Poly(witness, x)
        # Verify that the coefficients can be embedded in a field F
        F = p.domain.get_field()
        h1 = True
    except Exception:
        h1 = False

    try:
        if isinstance(witness, Poly):
            p = witness
        else:
            p = Poly(witness, x)
        # Verify that it is a polynomial in a single variable
        h2 = len(p.gens) == 1
    except Exception:
        h2 = False

    try:
        if isinstance(witness, Poly):
            p = witness
        else:
            p = Poly(witness, x)
            
        # Work over the field of fractions to properly check irreducibility over F
        F = p.domain.get_field()
        p_field = p.set_domain(F)
        
        # The quotient ring F[x]/(f(x)) is a field iff f(x) is irreducible over F
        # and has degree >= 1.
        is_irred = p_field.is_irreducible
        
        if is_irred is None:
            neg_q = False
        else:
            is_field = is_irred and p_field.degree() > 0
            neg_q = not is_field
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: Polynomial ring over F",
    "not Q: The quotient ring is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import symbols

x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_proper_ideal', False))
            h2 = bool(witness.get('is_ideal_of_polynomials', False))
            neg_q = not bool(witness.get('is_isomorphic', True))
            return [h1, h2, neg_q]
        except Exception:
            pass

    try:
        h1 = bool(witness.is_proper_ideal())
        h2 = bool(witness.is_ideal_of_polynomials())
        neg_q = not bool(witness.is_isomorphic())
        return [h1, h2, neg_q]
    except AttributeError:
        pass

    try:
        h1 = bool(witness.is_proper_ideal)
        h2 = bool(witness.is_ideal_of_polynomials)
        neg_q = not bool(witness.is_isomorphic)
        return [h1, h2, neg_q]
    except AttributeError:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "H_2: I(x) is the ideal of R(x) consisting of all polynomials with coefficients in I",
    "¬Q: The factor ring R(x)/I(x) is not isomorphic to the polynomial ring (R/I)(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2
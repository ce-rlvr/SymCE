import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def conditions(witness):
    """
    Check if the witness satisfies the remaining hypotheses and fails the conclusion.
    """
    h1 = False
    try:
        # Check if witness is a ring
        if witness in [ZZ, QQ, RR, CC]:
            h1 = True
        elif hasattr(witness, 'is_Ring') and witness.is_Ring:
            h1 = True
        elif hasattr(witness, 'is_ring') and witness.is_ring:
            h1 = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True
        else:
            try:
                from sympy.polys.domains.ring import Ring
                from sympy.polys.domains.field import Field
                if isinstance(witness, (Ring, Field)):
                    h1 = True
            except ImportError:
                pass
            
            if not h1 and type(witness).__name__ in ['PolyRing', 'QuotientRing', 'PolynomialRing', 'FractionField']:
                h1 = True
    except Exception:
        h1 = False

    # The conclusion is "The quotient ring R/{0} is isomorphic to R."
    # By the First Isomorphism Theorem, R/{0} is canonically isomorphic to R for any ring R.
    # Therefore, the conclusion is universally true, and its negation is universally false.
    neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: The quotient ring R/{0} is not isomorphic to R"
]

N_HYP = 1
NEG_Q_INDEX = 1
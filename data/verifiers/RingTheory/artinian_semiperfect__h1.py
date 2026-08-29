import sympy
from sympy import ZZ, QQ, RR, CC, S
from sympy.abc import x, y, z

# Top-level setup
# Standard rings are imported above and available in the namespace.

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    def is_semiperfect(ring):
        # Fields are local rings, hence semiperfect
        if getattr(ring, 'is_Field', False):
            return True
        if ring in (S.Reals, S.Rationals, S.Complexes):
            return True
        # Finite rings like Z/nZ are Artinian, hence semiperfect
        if ring.__class__.__name__ == 'IntegerModRing':
            return True
        # The ring of integers Z is not semiperfect (infinitely many maximal ideals)
        if ring == ZZ or ring == S.Integers:
            return False
        # Polynomial rings over a domain are not semiperfect
        if ring.__class__.__name__ in ('PolynomialRing', 'PolyRing'):
            return False
        raise ValueError("Unknown ring")

    try:
        semiperfect = is_semiperfect(witness)
        neg_q = not semiperfect
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = ["¬Q: R is not a semiperfect ring"]
N_HYP = 0
NEG_Q_INDEX = 0